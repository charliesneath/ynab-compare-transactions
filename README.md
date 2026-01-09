# YNAB Transaction Comparison Tool

A Python CLI tool to identify discrepancies between your Chase bank account and YNAB budget by comparing transactions.

## Features

- Parse Chase CSV transaction exports
- Fetch transactions from YNAB via API
- Identify missing transactions in either system
- Find amount mismatches
- Balance verification

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your YNAB Personal Access Token:
   - Go to https://app.ynab.com/settings/developer
   - Create a new Personal Access Token
   - Save it securely

3. Export your Chase transactions:
   - Log into Chase online banking
   - Navigate to your account
   - Download transactions as CSV

## Usage

```bash
python compare.py --chase transactions.csv --ynab-token YOUR_TOKEN --budget-name "My Budget" --account-name "Chase Checking"
```

### Arguments

- `--chase` - Path to Chase CSV export file
- `--ynab-token` - Your YNAB Personal Access Token
- `--budget-name` - Name of your YNAB budget
- `--account-name` - Name of the YNAB account to compare
- `--date-from` (optional) - Start date for comparison (YYYY-MM-DD)
- `--date-to` (optional) - End date for comparison (YYYY-MM-DD)

## Output

The tool will show:
- Transactions in Chase but missing in YNAB
- Transactions in YNAB but missing in Chase
- Balance comparison
