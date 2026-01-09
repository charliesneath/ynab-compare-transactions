# Reconciliation Report - 2026-01-09

**Date Range:** 2025-11-12 to 2026-01-08
**Chase Balance:** $30,438.35
**YNAB Balance:** $63,538.35
**Discrepancy:** $33,100.00 (YNAB shows MORE than Chase)

---

## Analysis

### Issue: YNAB thinks there's $33,100 MORE in the account than there actually is.

This means either:
1. Transactions are missing from YNAB (inflows not recorded)
2. Transactions are duplicated or incorrect in YNAB (outflows not recorded or inflows doubled)

---

## TRANSACTIONS TO ADD TO YNAB

These are in Chase but missing from YNAB. Add these to your YNAB account:

### High Priority (Large Amounts)

1. **2025-12-08** | **+$50,000.00** | AMERICAN EXPRESS TRANSFER
   - **Action:** Add this $50,000 INFLOW to YNAB
   - **Note:** This might be related to the Dec 5 transfer you have in YNAB

2. **2025-12-29** | **+$25,000.00** | AMERICAN EXPRESS TRANSFER
   - **Action:** Add this $25,000 INFLOW to YNAB
   - **Note:** This might be related to the Dec 26 transfer you have in YNAB

### Lower Priority (Checks and Transfers)

3. **2025-11-21** | **-$175.00** | CHECK 384
   - **Action:** Add this $175 OUTFLOW to YNAB
   - **Payee:** Check the check register or memo for who this was paid to

4. **2025-11-26** | **-$100.00** | Online Transfer to Citizens Checking
   - **Action:** Add this $100 transfer OUT to YNAB
   - **Category:** Transfer to Citizens Checking account

5. **2025-12-05** | **-$175.00** | CHECK 390
   - **Action:** Add this $175 OUTFLOW to YNAB
   - **Payee:** Check the check register

6. **2025-12-19** | **-$175.00** | CHECK 399
   - **Action:** Add this $175 OUTFLOW to YNAB
   - **Payee:** Check the check register

---

## TRANSACTIONS IN YNAB TO INVESTIGATE

These are in YNAB but NOT in the Chase CSV. Need to verify these:

### Possible Duplicates or Errors

1. **2025-11-18** | **-$175.00** | Silas & Maria Cleaning
   - **Question:** Is this a duplicate? Similar amount to CHECK 384 ($175 on 11/21)
   - **Action:** Verify this is a separate transaction from the check

2. **2025-11-24** | **-$1,200.00** | CHECK # 385
   - **Action:** Verify this check cleared. If not in Chase CSV, it may be pending or entered incorrectly

3. **2025-12-02** | **-$175.00** | Silas & Maria Cleaning
   - **Question:** Is this related to CHECK 390 ($175 on 12/05)?
   - **Action:** Verify separate transaction

4. **2025-12-16** | **-$175.00** | Silas & Maria Cleaning
   - **Question:** Is this related to CHECK 399 ($175 on 12/19)?
   - **Action:** Verify separate transaction

### Transfer Transactions (Likely Correct)

5. **2025-12-05** | **+$50,000.00** | Transfer : Joint Savings Account
   - **Note:** This is likely the SAME as the Dec 8 Amex transfer in Chase
   - **Action:** If this matches the Chase transaction, UPDATE THE DATE to 12/08 and change description to "AMERICAN EXPRESS TRANSFER"

6. **2025-12-26** | **+$25,000.00** | Transfer : Joint Savings Account
   - **Note:** This is likely the SAME as the Dec 29 Amex transfer in Chase
   - **Action:** If this matches the Chase transaction, UPDATE THE DATE to 12/29 and change description to "AMERICAN EXPRESS TRANSFER"

7. **2026-01-09** | **+$30,000.00** | Transfer : Joint Savings Account
   - **Note:** This is AFTER the CSV export date (2026-01-08)
   - **Action:** This is fine - it's a future/pending transaction not yet in the bank statement

### Additional Checks to Investigate

8. **2025-12-29** | **-$1,200.00** | CHECK # 394
   - **Action:** Verify this check cleared

9. **2025-12-29** | **-$1,200.00** | CHECK # 449
   - **Action:** Verify this check cleared

10. **2025-12-29** | **-$1,200.00** | CHECK # 402
    - **Action:** Verify this check cleared

---

## RECOMMENDED RECONCILIATION STEPS

### Step 1: Fix the Large Transfers (This will fix $33,100 - most of the discrepancy!)

The two big Amex transfers are likely already in YNAB but with wrong dates:

**In YNAB, find these transactions:**
- 2025-12-05 | +$50,000 | Transfer : Joint Savings Account
- 2025-12-26 | +$25,000 | Transfer : Joint Savings Account

**Update them to match Chase:**
- Change Dec 5 → Dec 8 (and update description to "AMERICAN EXPRESS TRANSFER")
- Change Dec 26 → Dec 29 (and update description to "AMERICAN EXPRESS TRANSFER")

**Expected impact:** This should reduce the discrepancy significantly

### Step 2: Add the Missing Checks

Add these to YNAB:
- 2025-11-21 | -$175 | CHECK 384
- 2025-12-05 | -$175 | CHECK 390
- 2025-12-19 | -$175 | CHECK 399

**Expected impact:** -$525 total

### Step 3: Add the Transfer to Citizens

- 2025-11-26 | -$100 | Transfer to Citizens Checking

**Expected impact:** -$100

### Step 4: Verify the Cleaning Payments

Check if these cleaning payments match the checks above (same amounts, close dates):
- If they're the same, delete the duplicate
- If they're different, they're correct as-is

### Step 5: Investigate Outstanding Checks

The three $1,200 checks (#394, #449, #402) all dated 12/29 aren't in the Chase CSV. Either:
- They haven't cleared yet (pending)
- They were entered in YNAB but not actually written
- They cleared after the CSV export date

**Action:** Check your actual check register or wait for them to clear

---

## After Making Changes

Run the tool again:
```bash
python compare.py --chase data/Chase2567_Activity_20260109.CSV
```

The balance difference should be much smaller (hopefully $0)!
