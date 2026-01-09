#!/usr/bin/env python3
"""Side-by-side comparison of Chase vs YNAB transactions."""

import sys
from datetime import datetime, timedelta
from chase_parser import parse_chase_csv
from ynab_client import YNABClient
from decimal import Decimal

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

print("=" * 120)
print(f"RECONCILIATION COMPARISON: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
print("=" * 120)
print(f"Chase CSV: {len(chase_trans)} transactions")
print(f"YNAB (unreconciled): {len(ynab_trans)} transactions")
print()
print("Matching logic: YNAB date can be within ±5 days of Chase date")
print("               Amount must match exactly")
print()

# Match transactions with tolerance
matched_chase = set()
matched_ynab = set()
matches = []

for i, ct in enumerate(chase_trans):
    for j, yt in enumerate(ynab_trans):
        if j in matched_ynab:
            continue

        # Check if amounts match
        if abs(float(ct.amount) - float(yt.amount)) < 0.01:
            # Check if YNAB date is within ±5 days of Chase date
            date_diff = (yt.date - ct.date).days
            if -5 <= date_diff <= 5:
                matches.append((i, j, ct, yt, date_diff))
                matched_chase.add(i)
                matched_ynab.add(j)
                break

# Find unmatched
unmatched_chase = [(i, t) for i, t in enumerate(chase_trans) if i not in matched_chase]
unmatched_ynab = [(i, t) for i, t in enumerate(ynab_trans) if i not in matched_ynab]

print("=" * 120)
print("TRANSACTIONS THAT DON'T MATCH")
print("=" * 120)
print(f"{'IN CHASE, NOT IN YNAB':<55} | {'IN YNAB, NOT IN CHASE':<55}")
print("-" * 120)

# Print side by side
max_len = max(len(unmatched_chase), len(unmatched_ynab))
for i in range(max_len):
    chase_str = ""
    ynab_str = ""

    if i < len(unmatched_chase):
        _, ct = unmatched_chase[i]
        chase_str = f"{ct.date} ${ct.amount:>10.2f} {ct.description[:28]}"

    if i < len(unmatched_ynab):
        _, yt = unmatched_ynab[i]
        ynab_str = f"{yt.date} ${yt.amount:>10.2f} {yt.payee_name[:28]}"

    print(f"{chase_str:<55} | {ynab_str:<55}")

print()
print("=" * 120)
print("SUMMARY")
print("=" * 120)
print(f"Matched: {len(matches)} transactions")
print(f"In Chase, not in YNAB: {len(unmatched_chase)} transactions (ADD to YNAB)")
print(f"In YNAB, not in Chase: {len(unmatched_ynab)} transactions (INVESTIGATE)")
print()

# Calculate totals
chase_total = sum(float(t.amount) for _, t in unmatched_chase)
ynab_total = sum(float(t.amount) for _, t in unmatched_ynab)

print(f"Unmatched Chase total: ${chase_total:,.2f}")
print(f"Unmatched YNAB total: ${ynab_total:,.2f}")
print(f"Net difference: ${chase_total - ynab_total:,.2f}")
