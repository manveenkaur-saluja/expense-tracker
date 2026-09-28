import pandas as pd
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self, file_name):
        self.filename = file_name

        if not os.path.exists(self.filename):
            df = pd.DataFrame(
                columns=["ID", "Category", "Amount", "Date", "Time"]
            )
            df.to_csv(self.filename, index=False)

    def add(self, category, amount):
        
        df = pd.read_csv(self.filename)

        new_id = len(df) + 1

        new_data = {
            "ID": new_id,
            "Category": category,
            "Amount": float(amount),
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.now().strftime("%H:%M:%S")
        }

        new_row = pd.DataFrame([new_data])

        new_row.to_csv(
            self.filename,
            mode="a",
            header=False,
            index=False
        )
        print(f"The Rs{amount} spend in {category} is successfully added to your Expense Tracker.")

    def view_all(self):
        if not os.path.exists(self.filename):
            print("No expenses recorded yet.")
            return

        df = pd.read_csv(self.filename)

        total_spending = df["Amount"].sum()

        if df.empty:
            print("No expenses recorded yet.")
            return

        print(df.to_string(index=False))
        print(f"\nYour total spending is : {total_spending}")

    def delete(self):
        command = int(input('Enter the ID to delete: '))

        df = pd.read_csv(self.filename)
        
        if command not in df["ID"].values:
            print("Expenses ID not Found")
            return

        df = df[df["ID"] != command]

        df["ID"] = range(1, len(df) + 1)
        
        df.to_csv(self.filename, index=False)

    def update(self):
        command = input("What you want to update(Category/Amount/Date): ").lower()
        id = int(input("enter the ID which is belongs: "))

        updated = False

        df = pd.read_csv(self.filename)

        if command == "category" and id in df["ID"].values:
            new_value = input("Enter new value: ")
            df.loc[df["ID"] == id, "Category"] = new_value
            updated = True

        elif command == "amount" and id in df["ID"].values:
            new_value = float(input("Enter new value: "))
            df.loc[df["ID"] == id, "Amount"] = new_value
            updated = True

        elif command == "date" and id in df["ID"].values:
            new_value = input("Enter new value: ")
            df.loc[df["ID"] == id, "Date"] = new_value
            updated = True


        else:
            print("Invalid Description or ID")

        if updated:
            df.to_csv(self.filename, index=False)
            print("Updated successfully")


user_1 = ExpenseTracker("Expense.csv")
user_1.add("Recharge", "750")
