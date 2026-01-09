# Agent Guide: Using the YNAB Comparison Tool for Reconciliation

## Purpose

This CLI tool helps reconcile YNAB accounts with bank statements (Chase CSV exports) by identifying discrepancies between what the bank says and what YNAB says.

## Understanding Reconciliation

**Reconciliation** in YNAB means confirming that YNAB's recorded balance matches the bank's actual balance. When these don't match, there are missing or incorrect transactions in YNAB.

### Key Concepts

1. **Chase Balance** - The actual balance from the bank (the source of truth)
2. **YNAB Balance** - What YNAB thinks the balance is
3. **Difference** - The reconciliation gap that needs to be resolved
4. **Last Reconciled Date** - The last time the user confirmed YNAB matched the bank

## The Problem

When YNAB shows a different balance than Chase:
- YNAB Balance > Chase Balance = YNAB has extra money recorded (transactions missing in YNAB or recorded incorrectly)
- YNAB Balance < Chase Balance = YNAB is missing money (transactions in YNAB that shouldn't be there or amounts wrong)

The discrepancy exists somewhere between the last reconciliation date and the current CSV export date.

## How to Use This Tool

### Step 1: Run the Comparison

```bash
python compare.py --chase data/chase-export.csv
```

The tool automatically:
- Parses the Chase CSV
- Identifies the date range in the CSV
- Fetches YNAB transactions for the same date range
- Compares transactions
- Reports discrepancies

### Step 2: Understand the Output

The tool shows:

```
================================================================================
BALANCE COMPARISON
================================================================================
Chase Balance:       $30,438.35
YNAB Balance:        $63,538.35
Difference:          $-33,100.00
```

**This means:** YNAB thinks there's $33,100 MORE in the account than Chase says there is.

```
================================================================================
TRANSACTIONS IN CHASE BUT NOT IN YNAB (6)
================================================================================
2025-12-08 | $  50000.00 | AMERICAN EXPRESS TRANSFER
```

**This means:** These transactions happened at the bank but aren't recorded in YNAB. They need to be added.

```
================================================================================
TRANSACTIONS IN YNAB BUT NOT IN CHASE (10)
================================================================================
2025-12-05 | $  50000.00 | Transfer : Joint Savings Account
```

**This means:** YNAB has these transactions recorded, but they don't appear in the bank statement. They might be:
- Duplicates in YNAB
- Transfers between accounts (not shown in bank CSV)
- Incorrectly entered transactions
- Pending transactions that haven't cleared yet

## Step 3: Reconciliation Workflow

### For transactions in Chase but not in YNAB:
1. These are MISSING from YNAB and should be added
2. Add each transaction to YNAB manually or via import
3. Verify the amount and date match

### For transactions in YNAB but not in Chase:
1. **Check if they're transfers** - Transfers between YNAB accounts won't show in individual bank statements
2. **Check the dates** - Pending transactions in YNAB might not have cleared yet
3. **Check for duplicates** - User might have entered the transaction twice
4. **Verify descriptions** - Same transaction might have different descriptions

### Important: Matching Logic

The tool uses fuzzy matching with:
- **Date tolerance**: ±2 days (configurable with `--tolerance-days`)
- **Amount tolerance**: ±$0.01 (for rounding differences)

Transactions that are "close" in date and amount might be the same transaction with different descriptions.

## Step 4: Common Scenarios

### Scenario 1: Large transfers showing as mismatches

```
Chase: 2025-12-08 | $50000.00 | AMERICAN EXPRESS TRANSFER
YNAB:  2025-12-05 | $50000.00 | Transfer : Joint Savings Account
```

**Likely reason:** Same transaction, different descriptions. The dates are close (within 3 days).

**Action:** Verify these are the same transaction. If so, they're already matched - no action needed.

### Scenario 2: Balance difference equals sum of discrepancies

If the balance difference ($33,100) equals the sum of unmatched transactions, these ARE the cause of the discrepancy.

**Action:**
- Add missing Chase transactions to YNAB
- Remove or correct incorrect YNAB transactions
- Re-run the tool to verify

### Scenario 3: Checks not matching

```
Chase: CHECK 384 | $-175.00
YNAB:  Silas & Maria Cleaning | $-175.00
```

**Likely reason:** User entered a payee name in YNAB but Chase just shows "CHECK 384"

**Action:** Update YNAB transaction memo to include check number for future tracking

## Step 5: After Making Changes

1. Make corrections in YNAB based on the analysis
2. Re-run the comparison tool
3. Verify the balance difference decreases
4. When difference = $0.00, mark the account as reconciled in YNAB

## Advanced Usage

### Custom date range

```bash
python compare.py --chase data/export.csv --date-from 2025-12-01 --date-to 2025-12-31
```

### Adjust date matching tolerance

```bash
python compare.py --chase data/export.csv --tolerance-days 5
```

Increase tolerance for transactions that might take longer to clear.

## Tips for Agents

1. **Always check transfer transactions first** - They're the most common false positive
2. **Look for patterns** - Multiple checks of the same amount might be legitimate
3. **Consider timing** - Pending transactions won't appear in bank statements yet
4. **Large amounts are highest priority** - Focus on big discrepancies first
5. **Suggest systematic approach** - Work through transactions chronologically

## Expected Output for a Reconciled Account

```
================================================================================
BALANCE COMPARISON
================================================================================
Chase Balance:       $30,438.35
YNAB Balance:        $30,438.35
Difference:          $0.00

================================================================================
All transactions matched!
================================================================================
```

When you see this, the account is fully reconciled.

## Common Questions

**Q: Why are there so many YNAB transactions not in Chase?**
A: The tool now automatically filters to the Chase CSV date range, so this should be minimal. If you still see many, they're likely transfers or pending transactions.

**Q: Should I delete transactions in "YNAB but not in Chase"?**
A: No! Investigate first. Many are legitimate transfers or pending transactions.

**Q: The balance difference is huge. Where do I start?**
A: Start with the largest amounts first. Often 1-2 big transactions cause most of the discrepancy.

**Q: Can this tool fix YNAB automatically?**
A: No. This is a read-only analysis tool. The user must make corrections in YNAB manually.

## Files in This Project

- `compare.py` - Main CLI tool
- `chase_parser.py` - Parses Chase CSV exports
- `ynab_client.py` - YNAB API client
- `list_accounts.py` - Helper to list available budgets and accounts
- `.env` - User's credentials and configuration (not in git)
- `data/` - Place Chase CSV exports here (not in git)
