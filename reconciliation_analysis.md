# Reconciliation Analysis - Excluding Expected $30k Transfer

## Adjusted Balance Calculation

**Original:**
- Chase Balance: $30,438.35
- YNAB Balance: $63,538.35
- Difference: -$33,100.00

**Adjusting for expected $30k inflow (Jan 9):**
- Chase Balance: $30,438.35
- YNAB Balance (adjusted): $63,538.35 - $30,000 = $33,538.35
- **Remaining Difference: -$3,100.00**

---

## We Need to Find $3,100 in Discrepancies

### Transactions in Chase NOT in YNAB

1. **2025-11-26 | -$100.00** | Transfer to Citizens Checking
   - **Impact:** YNAB is $100 too high (missing outflow)
   - **Action:** Add this to YNAB

**Subtotal: $100 of the $3,100 explained**

---

### Transactions in YNAB NOT in Chase (excluding the $30k)

These could be causing YNAB to be incorrect:

1. **2025-11-17 | -$4,000.00** | Online Payment To Julie Schaeffer
2. **2025-11-24 | -$1,200.00** | CHECK # 385
3. **2025-12-24 | -$4,000.00** | CHECK # 400 (Modern Interiors)
4. **2025-12-29 | -$1,200.00** | CHECK # 394
5. **2025-12-29 | -$1,200.00** | CHECK # 449
6. **2025-12-29 | -$1,200.00** | CHECK # 402

**Total in YNAB but not Chase: -$12,800**

---

## Critical Question

If these $12,800 in outflows are recorded in YNAB but haven't actually cleared the bank, that would make YNAB balance LOWER than it should be, not higher.

But YNAB is $3,100 HIGHER than Chase (after adjusting for the $30k).

This suggests one of these scenarios:

### Scenario A: Some of these are duplicates in YNAB
If you accidentally entered some transactions twice in YNAB, the balance would be too low.

### Scenario B: There are INFLOWS missing from YNAB
Are there any deposits or credits in the Chase CSV that aren't showing in YNAB?

### Scenario C: Some YNAB transactions have wrong amounts
Maybe some transactions are entered with incorrect amounts in YNAB.

---

## Let's Check the Chase CSV for Inflows

Let me look at the Chase CSV to see all the INFLOWS (positive amounts) that might be missing from YNAB.
