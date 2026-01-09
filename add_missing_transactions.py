#!/usr/bin/env python3
"""Reconcile YNAB: add missing transactions and remove duplicates with user approval."""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

from chase_parser import parse_chase_csv
from ynab_client import YNABClient
from compare import TransactionMatcher

load_dotenv()


def main():
    """Find discrepancies and ask for approval before making changes."""

    # Get configuration
    chase_csv = sys.argv[1] if len(sys.argv) > 1 else None
    if not chase_csv:
        print("Usage: python add_missing_transactions.py <chase-csv-file>")
        sys.exit(1)

    ynab_token = os.getenv("YNAB_TOKEN")
    budget_name = os.getenv("BUDGET_NAME")
    account_name = os.getenv("ACCOUNT_NAME")

    # Parse Chase CSV
    print("\n" + "=" * 80)
    print("📄 PARSING CHASE CSV EXPORT")
    print("=" * 80)
    print(f"File: {chase_csv}")

    chase_transactions = parse_chase_csv(chase_csv)

    if not chase_transactions:
        print("❌ No transactions found in CSV")
        sys.exit(1)

    # Get date range and most recent balance
    chase_dates = [t.date for t in chase_transactions]
    earliest_date = min(chase_dates)
    latest_date = max(chase_dates)

    # Most recent transaction has the current balance
    most_recent_trans = max(chase_transactions, key=lambda t: t.date)
    chase_current_balance = most_recent_trans.balance

    print(f"✅ Parsed {len(chase_transactions)} transactions")
    print(f"📅 Date range: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
    print(f"💰 Most recent balance (as of {latest_date.strftime('%Y-%m-%d')}): ${chase_current_balance:,.2f}")

    # Connect to YNAB
    print("Connecting to YNAB...")
    ynab = YNABClient(ynab_token)

    budget_id = ynab.get_budget_id(budget_name)
    if not budget_id:
        print(f"Budget '{budget_name}' not found")
        sys.exit(1)

    account_id = ynab.get_account_id(budget_id, account_name)
    if not account_id:
        print(f"Account '{account_name}' not found")
        sys.exit(1)

    # Get YNAB transactions and balance
    all_ynab_transactions = ynab.get_transactions(
        budget_id,
        account_id,
        since_date=earliest_date.strftime('%Y-%m-%d')
    )

    # Filter to only unreconciled transactions (YNAB reconciliation logic)
    # When reconciling, you only work with transactions that aren't already reconciled
    ynab_transactions = [
        t for t in all_ynab_transactions
        if t.cleared != "reconciled"
    ]

    reconciled_count = len(all_ynab_transactions) - len(ynab_transactions)

    print(f"Found {len(all_ynab_transactions)} YNAB transactions total")
    print(f"  • {len(ynab_transactions)} unreconciled (will compare)")
    print(f"  • {reconciled_count} already reconciled (will ignore)")

    # Get YNAB account details (using YNAB API's balances)
    account_details = ynab.get_account_details(budget_id, account_id)
    if not account_details:
        print(f"Error: Could not get account details")
        sys.exit(1)

    # YNAB's Reconciliation Logic uses "cleared_balance" from the API
    # This is the balance of all cleared and reconciled transactions
    ynab_cleared_balance = account_details["cleared_balance"]
    ynab_working_balance = account_details["balance"]
    ynab_uncleared_balance = account_details["uncleared_balance"]

    # Calculate reconciliation difference (YNAB's actual reconciliation logic)
    # This is exactly what YNAB shows when you enter the bank balance
    reconciliation_difference = ynab_cleared_balance - chase_current_balance

    # Show reconciliation status (mimicking YNAB UI)
    print("\n" + "=" * 80)
    print("🔄 RECONCILIATION - MATCHING YNAB'S LOGIC")
    print("=" * 80)
    print(f"\n📊 Reconciling '{account_details['name']}' to Chase balance:")
    print(f"   As of: {latest_date.strftime('%B %d, %Y')}")
    print(f"\n   Bank Balance (Chase):           ${chase_current_balance:>12,.2f}")
    print(f"   YNAB Cleared Balance:           ${ynab_cleared_balance:>12,.2f}")
    print(f"   " + "-" * 52)
    print(f"   Reconciliation Difference:      ${reconciliation_difference:>12,.2f}")

    if abs(reconciliation_difference) < 0.01:
        print(f"\n✅ Perfect! Your account is reconciled.")
        print(f"   The cleared balance in YNAB matches your bank balance.")
        sys.exit(0)
    elif reconciliation_difference > 0:
        print(f"\n⚠️  YNAB's cleared balance is ${abs(reconciliation_difference):,.2f} HIGHER than Chase")
        print(f"   Possible causes:")
        print(f"   • Transactions in Chase that aren't in YNAB (need to add)")
        print(f"   • Duplicate transactions in YNAB (need to remove)")
        print(f"   • Amounts entered incorrectly in YNAB")
    else:
        print(f"\n⚠️  YNAB's cleared balance is ${abs(reconciliation_difference):,.2f} LOWER than Chase")
        print(f"   Possible causes:")
        print(f"   • Transactions in YNAB that haven't cleared Chase yet")
        print(f"   • Missing inflows in YNAB that are in Chase")
        print(f"   • Amounts entered incorrectly in YNAB")

    # Show additional balance info if there are uncleared transactions
    if abs(ynab_uncleared_balance) > 0.01:
        print(f"\n📝 YNAB Balance Breakdown:")
        print(f"   • Cleared Balance:    ${ynab_cleared_balance:>12,.2f} (used for reconciliation)")
        print(f"   • Uncleared Balance:  ${ynab_uncleared_balance:>12,.2f} (pending transactions)")
        print(f"   • Working Balance:    ${ynab_working_balance:>12,.2f} (total)")

    # Compare and find discrepancies
    print("\nComparing transactions...")
    matcher = TransactionMatcher(tolerance_days=5)
    unmatched_chase, unmatched_ynab = matcher.compare_transactions(chase_transactions, ynab_transactions)

    # Filter out future transactions from YNAB (after CSV date range)
    latest_chase_date = max(chase_dates)
    unmatched_ynab_to_investigate = [
        t for t in unmatched_ynab
        if t.date <= latest_chase_date
    ]

    if not unmatched_chase and not unmatched_ynab_to_investigate:
        print("\n✅ Perfect! All transactions are reconciled.")
        sys.exit(0)

    # Section 1: Show transactions to ADD
    if unmatched_chase:
        print("\n" + "=" * 80)
        print(f"FOUND {len(unmatched_chase)} TRANSACTIONS IN CHASE BUT NOT IN YNAB")
        print("=" * 80)
        print("\n📋 Evidence from Chase CSV - These will be ADDED to YNAB:\n")

        for i, trans in enumerate(sorted(unmatched_chase, key=lambda t: t.date), 1):
            amount_str = f"+${trans.amount:.2f}" if trans.amount > 0 else f"-${abs(trans.amount):.2f}"
            balance_str = f"Balance after: ${trans.balance:.2f}" if trans.balance > 0 else ""
            trans_type = f"[{trans.transaction_type}]" if trans.transaction_type else ""

            print(f"{i}. {trans.date.strftime('%Y-%m-%d')} | {amount_str:>14} | {trans.description}")
            if trans_type or balance_str:
                print(f"   {trans_type} {balance_str}")

    # Section 2: Show transactions to INVESTIGATE (potential duplicates)
    if unmatched_ynab_to_investigate:
        print("\n" + "=" * 80)
        print(f"FOUND {len(unmatched_ynab_to_investigate)} TRANSACTIONS IN YNAB BUT NOT IN CHASE")
        print("=" * 80)
        print("\n⚠️  These may be duplicates, transfers, or incorrectly entered:\n")

        for i, trans in enumerate(sorted(unmatched_ynab_to_investigate, key=lambda t: t.date), 1):
            amount_str = f"+${trans.amount}" if trans.amount > 0 else f"-${abs(trans.amount)}"
            memo = f" ({trans.memo})" if trans.memo else ""
            print(f"{i}. {trans.date.strftime('%Y-%m-%d')} | {amount_str:>12} | {trans.payee_name}{memo}")

    # Ask for approval to ADD transactions
    transactions_to_add = []
    if unmatched_chase:
        print("\n" + "=" * 80)
        response = input(f"\nAdd {len(unmatched_chase)} missing transactions to YNAB? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            transactions_to_add = unmatched_chase
        else:
            print("⏭️  Skipping adding transactions.")

    # Ask for approval to DELETE transactions
    transactions_to_delete = []
    if unmatched_ynab_to_investigate:
        print("\n" + "=" * 80)
        print("\n⚠️  CAUTION: Only delete if you're SURE these are duplicates or errors!")
        print("Transfers between YNAB accounts won't show in bank statements.")
        response = input(f"\nDelete {len(unmatched_ynab_to_investigate)} YNAB transactions? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            transactions_to_delete = unmatched_ynab_to_investigate
        else:
            print("⏭️  Skipping deleting transactions.")

    if not transactions_to_add and not transactions_to_delete:
        print("\n❌ No changes made.")
        sys.exit(0)

    # Execute changes
    added_count = 0
    deleted_count = 0

    # Add transactions
    if transactions_to_add:
        print("\n" + "=" * 80)
        print("ADDING TRANSACTIONS TO YNAB")
        print("=" * 80)

        for trans in sorted(transactions_to_add, key=lambda t: t.date):
            try:
                ynab.create_transaction(
                    budget_id=budget_id,
                    account_id=account_id,
                    date=trans.date.strftime('%Y-%m-%d'),
                    amount=trans.amount,
                    payee_name=trans.description[:50],
                    memo=f"Added from Chase CSV on {datetime.now().strftime('%Y-%m-%d')}",
                    cleared="cleared"
                )

                amount_str = f"+${trans.amount}" if trans.amount > 0 else f"-${abs(trans.amount)}"
                print(f"✅ Added: {trans.date.strftime('%Y-%m-%d')} | {amount_str:>12} | {trans.description[:60]}")
                added_count += 1

            except Exception as e:
                print(f"❌ Failed: {trans.date.strftime('%Y-%m-%d')} | {trans.description[:60]}")
                print(f"   Error: {e}")

    # Delete transactions
    if transactions_to_delete:
        print("\n" + "=" * 80)
        print("DELETING TRANSACTIONS FROM YNAB")
        print("=" * 80)

        for trans in sorted(transactions_to_delete, key=lambda t: t.date):
            try:
                ynab.delete_transaction(budget_id, trans.transaction_id)

                amount_str = f"+${trans.amount}" if trans.amount > 0 else f"-${abs(trans.amount)}"
                memo = f" ({trans.memo})" if trans.memo else ""
                print(f"✅ Deleted: {trans.date.strftime('%Y-%m-%d')} | {amount_str:>12} | {trans.payee_name}{memo}")
                deleted_count += 1

            except Exception as e:
                print(f"❌ Failed: {trans.date.strftime('%Y-%m-%d')} | {trans.payee_name}")
                print(f"   Error: {e}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    if added_count > 0:
        print(f"✅ Added {added_count} transactions to YNAB")
    if deleted_count > 0:
        print(f"✅ Deleted {deleted_count} transactions from YNAB")

    print("\n🎉 Run compare.py again to verify the balance matches!")


if __name__ == "__main__":
    main()
