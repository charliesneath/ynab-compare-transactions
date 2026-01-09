"""Client for interacting with the YNAB API."""

import requests
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional


class YNABTransaction:
    """Represents a YNAB transaction."""

    def __init__(self, date: datetime, payee_name: str, amount: Decimal, memo: str, cleared: str, transaction_id: str):
        self.date = date
        self.payee_name = payee_name
        self.amount = amount  # YNAB stores in milliunits (divide by 1000)
        self.memo = memo
        self.cleared = cleared
        self.transaction_id = transaction_id

    def __repr__(self):
        return f"YNABTransaction(date={self.date.strftime('%Y-%m-%d')}, payee='{self.payee_name}', amount={self.amount})"


class YNABClient:
    """Client for the YNAB API."""

    BASE_URL = "https://api.ynab.com/v1"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str) -> Dict:
        """Make a request to the YNAB API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_budgets(self) -> List[Dict]:
        """Get all budgets."""
        data = self._make_request("/budgets")
        return data.get("data", {}).get("budgets", [])

    def get_budget_id(self, budget_name: str) -> Optional[str]:
        """Get budget ID by name."""
        budgets = self.get_budgets()
        for budget in budgets:
            if budget["name"].lower() == budget_name.lower():
                return budget["id"]
        return None

    def get_accounts(self, budget_id: str) -> List[Dict]:
        """Get all accounts for a budget."""
        data = self._make_request(f"/budgets/{budget_id}/accounts")
        return data.get("data", {}).get("accounts", [])

    def get_account_id(self, budget_id: str, account_name: str) -> Optional[str]:
        """Get account ID by name."""
        accounts = self.get_accounts(budget_id)
        for account in accounts:
            if account["name"].lower() == account_name.lower():
                return account["id"]
        return None

    def get_transactions(
        self,
        budget_id: str,
        account_id: str,
        since_date: Optional[str] = None
    ) -> List[YNABTransaction]:
        """
        Get transactions for a specific account.

        Args:
            budget_id: The budget ID
            account_id: The account ID
            since_date: Optional date in YYYY-MM-DD format

        Returns:
            List of YNABTransaction objects
        """
        endpoint = f"/budgets/{budget_id}/accounts/{account_id}/transactions"
        if since_date:
            endpoint += f"?since_date={since_date}"

        data = self._make_request(endpoint)
        transactions = []

        for trans in data.get("data", {}).get("transactions", []):
            # YNAB amounts are in milliunits (1000 milliunits = 1 currency unit)
            # Negative amounts in YNAB are outflows, positive are inflows
            amount = Decimal(trans["amount"]) / 1000

            transaction = YNABTransaction(
                date=datetime.strptime(trans["date"], "%Y-%m-%d"),
                payee_name=trans.get("payee_name", ""),
                amount=amount,
                memo=trans.get("memo", ""),
                cleared=trans.get("cleared", ""),
                transaction_id=trans["id"]
            )
            transactions.append(transaction)

        return transactions

    def get_account_balance(self, budget_id: str, account_id: str) -> Decimal:
        """Get the current balance for an account."""
        accounts = self.get_accounts(budget_id)
        for account in accounts:
            if account["id"] == account_id:
                # Balance is in milliunits
                return Decimal(account["balance"]) / 1000
        return Decimal("0")
