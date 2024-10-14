# Main file that controls the flow of the program.

import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from data_entry import get_date, get_category, get_amount, get_description

# Create a class to share the csv filename constant.


class CSV:
    """
    A class to handle CSV file operations for financial data.

    This class provides methods to initialize the CSV file, add new rows, and
    retrieve transactions within a specified date range. The CSV file is used
    to store personal finance data including the date, amount, category, and
    description of each transaction.

    Attributes:
    CSV_FILE (str): The filename of the CSV file.
    CSV_COLUMNNAMES (list): The column names for the CSV file.
    FORMAT (str): The date format used for parsing and formatting dates.
    """
    CSV_FILE = "finance_data.csv"  # class attribute variable for csv filename
    # class attribute variable for csv file columns
    CSV_COLUMNNAMES = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    # 💡Class Method Decorator, can only access the class attributes but not the instance attributes.
    @classmethod
    # first argument must always be the class instance itself
    def initialize_csv_file(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # create an empty csv file with column names, if not found
            df = pd.DataFrame(columns=cls.CSV_COLUMNNAMES)
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod  # add a new row of csv file
    def add_csv_file_row(cls, date, amount, category, description):
        """
        Add a new row to the CSV file.

        This class method creates a new dictionary entry with the specified details
        and appends it to the CSV file.

        Parameters:
        date (str): The date of the transaction.
        amount (float): The amount of the transaction.
        category (str): The category of the transaction (e.g., Income, Expense).
        description (str): A short description of the transaction.

        Returns:
        None
        """
    # create a dictionary to add the new row column details
        new_row = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.CSV_COLUMNNAMES)
            writer.writerow(new_row)
            print("New row added successfully !!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """This is a function to display transaction details of the finance details for a user input date range.
        Arguments:
            start_date -- start date of the date range.
            end_date -- _end date of the date range.
        Returns:
            A filtered dataframe for the input date range._
        """
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        filter = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[filter]

        # display the date range transaction summary
        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(
                CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={
                  "date": lambda x: x.strftime(CSV.FORMAT)}))

        # summarize the amounts
        total_income = filtered_df[filtered_df["category"]
            == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"]
            == "Expense"]["amount"].sum()

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df

   
def add_user_entered_row_detail():
    """
    Get user input for a new transaction row and add it to the CSV file.
    This function prompts the user to enter the date, amount, category, and description
    of a transaction. The details are then added as a new row in the CSV file.

    Parameters:
    None

    Returns:
    None
    """
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_csv_file_row(date, amount, category, description)


def plot_transactions(df):
    """
    Plot income and expenses over time from the transactions DataFrame.

    This function modifies the input DataFrame to use the date column as the index.
    It resamples the data to a daily frequency, fills missing dates with zero,
    and then plots the income and expenses over time.

    Parameters:
    df (DataFrame): A DataFrame containing transaction data with columns
                    'date', 'amount', 'category', and 'description'.

    Returns:
    None

    Side Effects:
    Displays a plot of income and expenses over the specified date range.
    """
    df.set_index("date", inplace=True) #using date column to locate the rows & modify the dataframe in place

    df_income = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0) # resample for daily frequency
    df_expense = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0) # resample for daily frequency
    print("coming here")
    print(df_expense.head())
    plt.figure(figsize =(10,5))
    plt.plot(df_income.index, df_income["amount"], label = "Income", color="g") # plotting x - 'date' & y axis - filtered income amount
    plt.plot(df_expense.index, df_expense["amount"], label = "Expense", color="r") # plotting x - 'date' & y axis - filtered expense amount
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
        

def main():
    """
    Main function to handle user interactions through a simple menu interface.

    This function provides a menu for the user to add a new transaction, view
    transactions and a summary within a specified date range, or exit the program.
    It continuously prompts the user for input until they choose to exit.

    Menu Options:
    1. Add a new transaction
    2. View transactions and summary within a date range
    3. Exit

    Parameters:
    None

    Returns:
    None
    """
    while True:
        print("\n1. Add new transaction")
        print("\n2. View transactions and summary within a date range")
        print("\n3. Exit")

        choice = input("Enter your choice (1-3):")

        if choice == "1":
            add_user_entered_row_detail()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting....")
        else:
            print("Invalid choice, enter a valid choice (1-3)")

if __name__ == "__main__":
    main()
