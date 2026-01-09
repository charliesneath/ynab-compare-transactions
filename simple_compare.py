#!/usr/bin/env python3
"""Simple comparison: just list what's in CSV vs YNAB, no fuzzy matching."""

import sys
from datetime import datetime
from chase_parser import parse_chase_csv
from ynab_client import YNABClient

# Load data
chase_csv = sys.argv[1] if len(sys.argv) > 1 else "data/Chase2567_Activity_20260109.CSV"
chase_trans = parse_chase_csv(chase_csv)

ynab = YNABClient("wYl-YCUhrOYPO4qIQ9U9cX_SiY2ul-NBLqGf3i2sFf4")
budget_id = ynab.get_budget_id("Sneath Shared")
account_id = ynab.get_account_id(budget_id, "👩‍❤️‍💋‍👨 Chase Shared Checking")

# Get CSV date range
chase_dates = [t.date for t in chase_trans]
earliest_date = min(chase_dates)
latest_date = max(chase_dates)

# Get YNAB transactions in same date range, exclude reconciled
all_ynab = ynab.get_transactions(budget_id, account_id, since_date=earliest_date.strftime('%Y-%m-%d'))
ynab_trans = [t for t in all_ynab if t.cleared != "reconciled" and t.date <= latest_date]

print("=" * 80)
print(f"CSV DATE RANGE: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
print("=" * 80)
print(f"Chase CSV: {len(chase_trans)} transactions")
print(f"YNAB (unreconciled, in range): {len(ynab_trans)} transactions")
print()

# Create sets of (date, amount) tuples for simple matching
chase_set = {(t.date, float(t.amount)) for t in chase_trans}
ynab_set = {(t.date, float(t.amount)) for t in ynab_trans}

# Find differences
in_chase_not_ynab = chase_set - ynab_set
in_ynab_not_chase = ynab_set - chase_set

print("=" * 80)
print(f"IN CHASE CSV BUT NOT IN YNAB: {len(in_chase_not_ynab)}")
print("=" * 80)
for date, amount in sorted(in_chase_not_ynab):
    # Find the transaction to get description
    trans = [t for t in chase_trans if t.date == date and float(t.amount) == amount][0]
    print(f"{date} | ${amount:>10.2f} | {trans.description[:70]}")

print()
print("=" * 80)
print(f"IN YNAB BUT NOT IN CHASE CSV: {len(in_ynab_not_chase)}")
print("=" * 80)
for date, amount in sorted(in_ynab_not_chase):
    # Find the transaction to get payee
    trans = [t for t in ynab_trans if t.date == date and float(t.amount) == amount]
    if trans:
        t = trans[0]
        print(f"{date} | ${amount:>10.2f} | {t.payee_name}")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Transactions to ADD to YNAB: {len(in_chase_not_ynab)}")
print(f"Transactions to INVESTIGATE in YNAB: {len(in_ynab_not_chase)}")
