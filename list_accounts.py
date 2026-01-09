#!/usr/bin/env python3
"""List all YNAB budgets and accounts."""

import os
from dotenv import load_dotenv
from ynab_client import YNABClient

load_dotenv()

token = os.getenv("YNAB_TOKEN")
budget_name = os.getenv("BUDGET_NAME")

client = YNABClient(token)

print("=" * 80)
print("YNAB BUDGETS")
print("=" * 80)
budgets = client.get_budgets()
for budget in budgets:
    print(f"- {budget['name']} (ID: {budget['id']})")

print("\n" + "=" * 80)
print(f"ACCOUNTS IN '{budget_name}' BUDGET")
print("=" * 80)

budget_id = client.get_budget_id(budget_name)
if budget_id:
    accounts = client.get_accounts(budget_id)
    for account in accounts:
        closed = " [CLOSED]" if account.get("closed") else ""
        print(f"- {account['name']}{closed} (ID: {account['id']})")
else:
    print(f"Budget '{budget_name}' not found")
