# YNAB Reconciliation Tool - Demo Walkthrough

This is a complete demo of the reconciliation workflow, from downloading your Chase CSV to reconciling your YNAB account.

---

## Step 1: Download Chase CSV

1. Log into Chase online banking
2. Navigate to your checking account
3. Download transactions as CSV
4. Save to `data/` folder: `data/Chase2567_Activity_20260109.CSV`

---

## Step 2: Run the Reconciliation Tool

```bash
python add_missing_transactions.py data/Chase2567_Activity_20260109.CSV
```

---

## Step 3: Review the Analysis

The tool starts by parsing your Chase CSV and showing you the reconciliation status:

```
================================================================================
📄 PARSING CHASE CSV EXPORT
================================================================================
File: data/Chase2567_Activity_20260109.CSV
✅ Parsed 103 transactions
📅 Date range: 2025-11-12 to 2026-01-08
💰 Most recent balance (as of 2026-01-08): $30,438.35
```

**What this tells you:**
- Successfully loaded your Chase export
- Covers transactions from Nov 12, 2025 to Jan 8, 2026
- Your current Chase balance is $30,438.35

---

## Step 4: See YNAB Connection

```
Connecting to YNAB...
Found 103 YNAB transactions total
  • 103 unreconciled (will compare)
  • 0 already reconciled (will ignore)
```

**What this tells you:**
- Connected to your YNAB account
- Found 103 unreconciled transactions to compare
- Ignoring any already-reconciled transactions

---

## Step 5: Review the Reconciliation Difference

This is the **key insight** - it matches exactly what you see in YNAB when you click "Reconcile":

```
================================================================================
🔄 RECONCILIATION - MATCHING YNAB'S LOGIC
================================================================================

📊 Reconciling '👩‍❤️‍💋‍👨 Chase Shared Checking' to Chase balance:
   As of: January 08, 2026

   Bank Balance (Chase):           $   30,438.35
   YNAB Cleared Balance:           $   33,748.77
   ----------------------------------------------------
   Reconciliation Difference:      $    3,310.42

⚠️  YNAB's cleared balance is $3,310.42 HIGHER than Chase
   Possible causes:
   • Transactions in Chase that aren't in YNAB (need to add)
   • Duplicate transactions in YNAB (need to remove)
   • Amounts entered incorrectly in YNAB
```

**What this tells you:**
- YNAB thinks you have $3,310.42 MORE than you actually have
- This is the exact same $3,310.42 that YNAB shows when you reconcile
- The tool explains possible causes

---

## Step 6: See Balance Breakdown

```
📝 YNAB Balance Breakdown:
   • Cleared Balance:    $   33,748.77 (used for reconciliation)
   • Uncleared Balance:  $   29,789.58 (pending transactions)
   • Working Balance:    $   63,538.35 (total)
```

**What this tells you:**
- Cleared balance ($33,748.77) is what YNAB uses for reconciliation
- Uncleared balance ($29,789.58) includes pending transactions
- Working balance ($63,538.35) is your total in YNAB

---

## Step 7: Review Transactions to ADD to YNAB

The tool shows you transactions that exist in Chase but are missing from YNAB:

```
================================================================================
FOUND 1 TRANSACTIONS IN CHASE BUT NOT IN YNAB
================================================================================

📋 Evidence from Chase CSV - These will be ADDED to YNAB:

1. 2025-11-26 |       -$100.00 | Online Transfer 26766127435 to Citizens Checking ######1313 transaction #: 26766127435 11/26
   [ACCT_XFER] Balance after: $90595.19
```

**What this tells you:**
- 1 transaction in Chase that's not in YNAB
- Shows the amount, date, and description from the CSV
- Shows transaction type [ACCT_XFER] and balance after
- This is concrete evidence from your bank statement

---

## Step 8: Review Transactions to INVESTIGATE

The tool shows transactions in YNAB that don't appear in your Chase CSV:

```
================================================================================
FOUND 6 TRANSACTIONS IN YNAB BUT NOT IN CHASE
================================================================================

⚠️  These may be duplicates, transfers, or incorrectly entered:

1. 2025-11-17 |       -$4000 | Online Payment 26918077338 To Julie Schaeffer 11/17
2. 2025-11-24 |       -$1200 | CHECK # 385
3. 2025-12-24 |       -$4000 | CHECK # 400 (Modern Interiors)
4. 2025-12-29 |       -$1200 | CHECK # 394
5. 2025-12-29 |       -$1200 | CHECK # 449
6. 2025-12-29 |       -$1200 | CHECK # 402
```

**What this tells you:**
- 6 transactions in YNAB that don't appear in Chase CSV
- These need investigation - they might be:
  - Transfers between YNAB accounts (won't show in individual bank statements)
  - Pending transactions that haven't cleared yet
  - Duplicates or errors in YNAB

---

## Step 9: Approve Adding Missing Transactions

The tool asks for your confirmation before making any changes:

```
================================================================================

Add 1 missing transactions to YNAB? (yes/no):
```

**Your options:**
- Type `yes` or `y` to add the missing transaction(s)
- Type `no` or `n` to skip adding

**If you type `yes`:**

```
⏭️  Proceeding to add transactions...
```

**If you type `no`:**

```
⏭️  Skipping adding transactions.
```

---

## Step 10: Decide About Questionable Transactions

Next, it asks about the transactions that are in YNAB but not in Chase:

```
================================================================================

⚠️  CAUTION: Only delete if you're SURE these are duplicates or errors!
Transfers between YNAB accounts won't show in bank statements.

Delete 6 YNAB transactions? (yes/no):
```

**Your options:**
- Type `yes` or `y` to delete these transactions from YNAB
- Type `no` or `n` to keep them (recommended unless you're certain they're duplicates)

**⚠️ Important:** Usually you should type `no` here and investigate manually, because:
- Transfers between YNAB accounts won't show in individual bank statements
- Pending checks may not have cleared yet
- You want to verify these before deleting

---

## Step 11: See the Results

If you approved adding transactions, you'll see:

```
================================================================================
ADDING TRANSACTIONS TO YNAB
================================================================================
✅ Added: 2025-11-26 |     -$100.00 | Online Transfer 26766127435 to Citizens Checking ######1313...

================================================================================
SUMMARY
================================================================================
✅ Added 1 transactions to YNAB

🎉 Run compare.py again to verify the balance matches!
```

If you approved deleting transactions:

```
================================================================================
DELETING TRANSACTIONS FROM YNAB
================================================================================
✅ Deleted: 2025-11-24 |    -$1200.00 | CHECK # 385

================================================================================
SUMMARY
================================================================================
✅ Deleted 1 transactions from YNAB

🎉 Run compare.py again to verify the balance matches!
```

---

## Step 12: Verify Reconciliation

Run the comparison tool again to verify:

```bash
python compare.py --chase data/Chase2567_Activity_20260109.CSV
```

If everything is reconciled, you should see:

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

---

## Complete Example Session

Here's what a complete session looks like:

```bash
$ python add_missing_transactions.py data/Chase2567_Activity_20260109.CSV

# ... [All the analysis output shown above] ...

Add 1 missing transactions to YNAB? (yes/no): yes
⏭️  Proceeding to add transactions...

Delete 6 YNAB transactions? (yes/no): no
⏭️  Skipping deleting transactions.

================================================================================
ADDING TRANSACTIONS TO YNAB
================================================================================
✅ Added: 2025-11-26 |     -$100.00 | Online Transfer to Citizens Checking...

================================================================================
SUMMARY
================================================================================
✅ Added 1 transactions to YNAB

🎉 Run compare.py again to verify the balance matches!

$ python compare.py --chase data/Chase2567_Activity_20260109.CSV

# Verify the new balance...
```

---

## Tips for Using the Tool

1. **Always review before approving** - The tool shows you exactly what it will change
2. **Be careful with deletions** - Transfers between accounts won't show in bank CSVs
3. **Investigate questionable transactions manually** - Check your actual bank account
4. **Run verification after changes** - Use `compare.py` to confirm reconciliation
5. **Use the CSV evidence** - Transaction types and balances help verify accuracy

---

## Understanding the $3,310.42 Discrepancy

In this example:
- **Chase says:** $30,438.35
- **YNAB says:** $33,748.77
- **Difference:** $3,310.42

This means YNAB thinks you have $3,310.42 MORE than you actually do.

**Possible causes:**
- Missing outflows in YNAB (expenses not recorded)
- Duplicate inflows in YNAB (income recorded twice)
- Incorrect amounts in transactions

The tool helps you find and fix these by:
1. Showing what's in Chase but not YNAB (missing transactions)
2. Showing what's in YNAB but not Chase (possible duplicates)
3. Providing CSV evidence for each recommendation
