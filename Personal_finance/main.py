import csv
from datetime import datetime
import pandas as pd
import data_entry
import matplotlib.pyplot as plt

class CSV:
    csv_file = 'finance.csv'
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%m-%d-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except:
            csv_data = pd.DataFrame(columns = cls.COLUMNS)
            csv_data.to_csv(cls.csv_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount" : amount,
            "category" : category,
            "description" : description
        }
        with open(cls.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_summary(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found')
        else:
            print(f'Transactions from date {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}')
            print(filtered_df.to_string(index=False, formatters={'date': lambda x: x.strftime(cls.FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense =  filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print("\n")

            print(f'Total Income: {total_income: .2f}')
            print(f'Total Expense: {total_expense: .2f}')
            print(f'Total Expenditure: {total_income - total_expense}')

        return filtered_df

def get_data():
    try:
        CSV.initialize_csv()

        date = data_entry.get_datetime("Enter the date of transaction?",allow_default=True)
        amount = data_entry.get_amount()
        category = data_entry.get_category()
        description = data_entry.get_description()
    
        CSV.add_entry(date, amount, category, description)
        
    except Exception as e:
        print(str(e))

def plot_graph(df):
    df.set_index('date',inplace=True)

    income_df = (df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value = 0))
    expense_df = (df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value = 0))

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df['amount'], label = 'Income', color = 'g')
    plt.plot(expense_df.index, expense_df['amount'], label = 'Expense', color = 'r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True: 
        print(" 1. Add transactions ")
        print(" 2. View Summary ")
        print(" 3. Exit ")

        choice = int(input("enter your choice"))

        if choice == 1:
            get_data()
        elif choice == 2:
            start_date = data_entry.get_datetime("Enter the start date: ")
            end_date = data_entry.get_datetime("Enter the end date: ")
            df = CSV.get_summary(start_date, end_date)
            plot_graph(df)
        elif choice == 3:
            print('Exiting..')
            break
        else:
            print(" Invalid choice. Enter 1, 2 or 3")

if __name__ == '__main__':
    main()








