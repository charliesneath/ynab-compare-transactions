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
uv pip install -r requirements.txt
```

Or with uv sync (recommended):
```bash
uv sync
```

2. Configure your credentials:
   - Copy `.env.example` to `.env`
   - Get your YNAB Personal Access Token from https://app.ynab.com/settings/developer
   - Edit `.env` and add your token, budget name, and account name

3. Export your Chase transactions:
   - Log into Chase online banking
   - Navigate to your account
   - Download transactions as CSV

## Usage

### Simple (using .env configuration):

```bash
uv run compare.py --chase ~/Downloads/chase-transactions.csv
```

### With all arguments:

```bash
uv run compare.py --chase transactions.csv --ynab-token YOUR_TOKEN --budget-name "My Budget" --account-name "Chase Checking"
```

### Arguments

All arguments can be set via command line or in `.env` file:

- `--chase` - Path to Chase CSV export file (or `CHASE_CSV_PATH` in .env)
- `--ynab-token` - Your YNAB Personal Access Token (or `YNAB_TOKEN` in .env)
- `--budget-name` - Name of your YNAB budget (or `BUDGET_NAME` in .env)
- `--account-name` - Name of the YNAB account to compare (or `ACCOUNT_NAME` in .env)
- `--date-from` (optional) - Start date for comparison (YYYY-MM-DD)
- `--date-to` (optional) - End date for comparison (YYYY-MM-DD)
- `--tolerance-days` (optional) - Number of days tolerance for date matching (default: 2)

## Output

The tool will show:
- Transactions in Chase but missing in YNAB
- Transactions in YNAB but missing in Chase
- Balance comparison
