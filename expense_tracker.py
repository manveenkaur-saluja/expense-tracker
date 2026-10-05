import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt


class ExpenseTracker:
    def __init__(self, file_name):
        self.filename = f"{file_name}.csv"

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
        print(f"Rs{amount} spent on {category} was successfully added to your Expense Tracker.")


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
        print("Expense deleted successfully.")

    def update(self):
        command = input("What you want to update(Category/Amount/Date): ").lower()
        expense_id = int(input("enter the ID which is belongs: "))

        updated = False

        df = pd.read_csv(self.filename)

        if command == "category" and expense_id in df["ID"].values:
            new_value = input("Enter new value: ")
            df.loc[df["ID"] == expense_id, "Category"] = new_value
            updated = True

        elif command == "amount" and expense_id in df["ID"].values:
            new_value = float(input("Enter new value: "))
            df.loc[df["ID"] == expense_id, "Amount"] = new_value
            updated = True

        elif command == "date" and expense_id in df["ID"].values:
            new_value = input("Enter new value: ")
            df.loc[df["ID"] == expense_id, "Date"] = new_value
            updated = True


        else:
            print("Invalid Description or ID")

        if updated:
            df.to_csv(self.filename, index=False)
            print("Updated successfully")

    def summary(self):
        df = pd.read_csv(self.filename)

        if df.empty:
            print("No expenses recorded yet.")
            return

        full_summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        print("-----Your Full Summary-----\n")
        print(full_summary)
        print(f"Overall spent: {df['Amount'].sum()}")

    def search_filter(self):
        df =pd.read_csv(self.filename)
     
        search = input("Enter the category you want to know: ").strip().capitalize()

        if search not in df['Category'].values:
            print("No such category found in your tracker")

        else:
            result = df[df['Category']== search]
            total_spent = df[df['Category']== search]['Amount'].sum()
            print(result.to_string(index=False))
            print(f"\nYour total spent in {search} is : {total_spent}")

    def monthly_report(self, month):
        month = month.strip().capitalize()

        months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6,
                  'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12 }

        months_number = months.get(month)

        df = pd.read_csv(self.filename)

        df['Date'] = pd.to_datetime(df['Date']) # Convert string format into datetime format(int)
        df['Months'] = df['Date'].dt.month      # Extract month number from Date

        if months_number not in df['Months'].values:
            print("No Record found of this month.")

        else:
            monthly_spent = df[df["Months"]== months_number]['Amount'].sum() 
            print(f'Total spending in {month} is : {monthly_spent}')

    def visuals(self):
        df = pd.read_csv(self.filename)

        if df.empty:
            print("No expense recorded yet")
            return

        category_totals = df.groupby('Category')['Amount'].sum()

        visual_type =  input("Pie/Bar/Line :").lower()

        if visual_type == "pie":

            category_totals.plot(
               kind="pie", 
               autopct="%1.1f%%", 
               startangle=30, 
               figsize=(6, 6),
               title="Expense Breakdown by Category"
            )
    
            plt.ylabel("") 
            plt.show()

        elif visual_type == "bar":
             
            category_totals.sort_values().plot(
                kind="barh", 
                color="skyblue", 
                edgecolor="black",
                figsize=(10, 6)
                )

            plt.title("Total spending by category")
            plt.xlabel("Total Spent (₹)")
            plt.ylabel("Category")
            plt.grid(axis="x", linestyle="--", alpha=0.7)
            plt.show()

        elif visual_type == "line":

            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index("Date", inplace=True)
            
            monthly_trend = df["Amount"].resample("M").sum()
            
            monthly_trend.plot(
                kind="line", 
                marker="o", 
                color="green", 
                linewidth=2,
                figsize=(10, 5)
            )
            
            plt.title("Monthly Expense Trend")
            plt.xlabel("Month")
            plt.ylabel("Total Spent (₹)")
            plt.grid(True, linestyle=":", alpha=0.6)
            plt.show()

        else:
            print("Invalid visual type. Choose Pie, Bar, or Line.")
            

user_1 = ExpenseTracker("My_tracker")
user_1.add('Books', 800)