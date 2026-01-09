"""Parse Chase bank CSV transaction exports."""

import csv
from datetime import datetime
from decimal import Decimal
from typing import List, Dict


class ChaseTransaction:
    """Represents a Chase transaction."""

    def __init__(self, date: datetime, description: str, amount: Decimal, transaction_type: str, balance: Decimal):
        self.date = date
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance = balance

    def __repr__(self):
        return f"ChaseTransaction(date={self.date.strftime('%Y-%m-%d')}, desc='{self.description}', amount={self.amount})"


def parse_chase_csv(filepath: str) -> List[ChaseTransaction]:
    """
    Parse a Chase CSV export file.

    Chase CSV format typically has columns:
    - Transaction Date
    - Post Date
    - Description
    - Category
    - Type
    - Amount
    - Balance (optional)

    Args:
        filepath: Path to the Chase CSV file

    Returns:
        List of ChaseTransaction objects
    """
    transactions = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Chase CSV format can vary, so we'll handle common variations
            # Try to find the date column
            date_str = row.get('Transaction Date') or row.get('Posting Date') or row.get('Date')
            if not date_str:
                continue

            # Parse date (Chase typically uses MM/DD/YYYY)
            try:
                trans_date = datetime.strptime(date_str, '%m/%d/%Y')
            except ValueError:
                try:
                    trans_date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    continue

            # Get description
            description = row.get('Description', '').strip()

            # Get amount
            amount_str = row.get('Amount', '0').replace('$', '').replace(',', '').strip()
            try:
                amount = Decimal(amount_str)
            except:
                amount = Decimal('0')

            # Get type
            trans_type = row.get('Type', '').strip()

            # Get balance (may not always be present)
            balance_str = row.get('Balance', '0').replace('$', '').replace(',', '').strip()
            try:
                balance = Decimal(balance_str) if balance_str else Decimal('0')
            except:
                balance = Decimal('0')

            transaction = ChaseTransaction(
                date=trans_date,
                description=description,
                amount=amount,
                transaction_type=trans_type,
                balance=balance
            )
            transactions.append(transaction)

    return transactions


def get_date_range(transactions: List[ChaseTransaction]) -> tuple:
    """Get the date range from a list of transactions."""
    if not transactions:
        return None, None

    dates = [t.date for t in transactions]
    return min(dates), max(dates)


def calculate_total(transactions: List[ChaseTransaction]) -> Decimal:
    """Calculate the total amount from a list of transactions."""
    return sum(t.amount for t in transactions)
