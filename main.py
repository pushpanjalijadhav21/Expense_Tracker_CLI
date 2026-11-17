from expense_manager import ExpenseManager


def run_cli():
    manager = ExpenseManager('expenses.db')
    while True:
        print('\n=== SYNTECXHUB EXPENSE TRACKER CLI ===')
        print('1. Add Transaction   2. Monthly Summary')
        print('3. Delete Record     4. Export Monthly CSV   5. Exit')
        choice = input('Select option (1-5): ').strip()

        if choice == '1':
            try:
                d = input('Date (YYYY-MM-DD): ').strip()
                t = input('Type (INCOME/EXPENSE): ').strip()
                c = input('Category: ').strip()
                a = float(input('Amount (INR): ').strip())
                n = input('Note: ').strip()
                row_id = manager.add_transaction(d, t, c, a, n)
                print(f'[SUCCESS] Saved transaction ID #{row_id}')
            except ValueError as err:
                print(f'[ERROR] Invalid input: {err}')

        elif choice == '2':
            m = input('Enter month (YYYY-MM): ').strip()
            s = manager.get_monthly_summary(m)
            print(f"\n--- Summary for {s['month']} ---")
            print(f"Total Income  : INR {s['total_income']:.2f}")
            print(f"Total Expense : INR {s['total_expense']:.2f}")
            print(f"Net Savings   : INR {s['net_savings']:.2f}")
            if s['by_category']:
                print("Category Breakdown:")
                for cat, amt in s['by_category'].items():
                    print(f"  - {cat}: INR {amt:.2f}")

        elif choice == '3':
            try:
                tx_id = int(input('Enter Transaction ID to delete: ').strip())
                if manager.delete_transaction(tx_id):
                    print(f'[SUCCESS] Deleted record #{tx_id}')
                else:
                    print('[INFO] Record ID not found.')
            except ValueError:
                print('[ERROR] Please enter a valid numeric ID.')

        elif choice == '4':
            m = input('Enter month to export (YYYY-MM): ').strip()
            out = f'exports/expense_report_{m}.csv'
            cnt = manager.export_month_csv(m, out)
            print(f'[EXPORTED] {cnt} record(s) written to {out}')

        elif choice == '5':
            print('Exiting Expense Tracker CLI. Goodbye!')
            break
        else:
            print('[ERROR] Invalid choice. Select 1-5.')


if __name__ == '__main__':
    run_cli()
