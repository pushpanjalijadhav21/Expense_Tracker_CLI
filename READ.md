# Expense Tracker CLI — SYNTECXHUB Python Programming Internship

A lightweight, zero-dependency command-line personal finance ledger built with **Python 3** and **SQLite3** as the capstone project for the **SYNTECXHUB Python Programming Internship** (Certificate ID: `SH07PPiXMZGwvdL6`).

## Features
- **Transaction Management:** Add and delete daily `INCOME` and `EXPENSE` entries with strict date (`YYYY-MM-DD`) and positive currency validation.
- **SQLite3 Persistence:** Automatically initializes `expenses.db` with parameterized SQL queries to prevent SQL injection.
- **Monthly Financial Analytics:** Computes Total Income, Total Expense, Net Savings, and category-wise spending breakdowns.
- **CSV Report Export:** Exports filtered monthly ledgers into UTF-8 formatted `.csv` files inside the `exports/` directory.

## How to Run Locally
```bash
git clone [https://github.com/](https://github.com/)<your-username>/Expense-Tracker-CLI.git
cd Expense-Tracker-CLI
python main.py
