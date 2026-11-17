import sqlite3
import csv
from datetime import datetime
from pathlib import Path


class ExpenseManager:
    def __init__(self, db_path: str = 'expenses.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        query = '''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_date TEXT NOT NULL,
            tx_type TEXT NOT NULL CHECK(tx_type IN ('INCOME', 'EXPENSE')),
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            note TEXT DEFAULT ''
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, tx_date: str, tx_type: str, category: str,
                        amount: float, note: str = '') -> int:
        datetime.strptime(tx_date, '%Y-%m-%d')
        tx_type_clean = tx_type.strip().upper()
        if tx_type_clean not in ('INCOME', 'EXPENSE'):
            raise ValueError('Transaction type must be INCOME or EXPENSE.')
        if amount <= 0:
            raise ValueError('Amount must be greater than zero.')
        cur = self.conn.execute(
            'INSERT INTO transactions (tx_date, tx_type, category, amount, note) '
            'VALUES (?, ?, ?, ?, ?)',
            (tx_date, tx_type_clean, category.strip().title(), round(amount, 2), note.strip())
        )
        self.conn.commit()
        return cur.lastrowid

    def get_monthly_summary(self, month_prefix: str) -> dict:
        cur = self.conn.execute(
            'SELECT tx_type, category, SUM(amount) AS total '
            'FROM transactions WHERE tx_date LIKE ? GROUP BY tx_type, category',
            (f'{month_prefix}%',)
        )
        income, expense, breakdown = 0.0, 0.0, {}
        for row in cur.fetchall():
            if row['tx_type'] == 'INCOME':
                income += row['total']
            else:
                expense += row['total']
                breakdown[row['category']] = round(row['total'], 2)
        return {
            'month': month_prefix,
            'total_income': round(income, 2),
            'total_expense': round(expense, 2),
            'net_savings': round(income - expense, 2),
            'by_category': breakdown
        }

    def delete_transaction(self, tx_id: int) -> bool:
        cur = self.conn.execute('DELETE FROM transactions WHERE id = ?', (tx_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def export_month_csv(self, month_prefix: str, filepath: str) -> int:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        rows = self.conn.execute(
            'SELECT id, tx_date, tx_type, category, amount, note '
            'FROM transactions WHERE tx_date LIKE ? ORDER BY tx_date ASC',
            (f'{month_prefix}%',)
        ).fetchall()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Date', 'Type', 'Category', 'Amount (INR)', 'Note'])
            for r in rows:
                writer.writerow([r['id'], r['tx_date'], r['tx_type'],
                                 r['category'], f"{r['amount']:.2f}", r['note']])
        return len(rows)
