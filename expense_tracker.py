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
        self.category = category.strip().capitalize()

        if not category:
           print("Category cannot be empty.")
           return

        try:
           amount = float(amount)

           if not amount > 0:
                print("Amount must be greater than zero.")
                return

        except ValueError:
           print("Please enter a valid numeric amount.")
           return

        df = pd.read_csv(self.filename)  

        new_id = int(df["ID"].max() or 0) + 1 if not df.empty else 1

        new_data = {
            "ID": new_id,
            "Category": self.category,
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
        print(f"Rs{amount} spent on {self.category} was successfully added to your Expense Tracker.")


    def view_all(self):
        df = pd.read_csv(self.filename)

        total_spending = df["Amount"].sum()

        if df.empty:
            print("No expenses recorded yet.")
            return

        print(df.to_string(index=False))
        print(f"\nYour total spending is : {total_spending}")

    def delete(self):
        df = pd.read_csv(self.filename)

        try:
            command = int(input('Enter the ID to delete: '))
            
            if command not in df["ID"].values:
                print("Expenses ID not Found")
                return
                
            df = df[df["ID"] != command]
    
            df["ID"] = range(1, len(df) + 1)
            
            df.to_csv(self.filename, index=False)
            print("Expense deleted successfully.")

        except ValueError:
            print("Its not a valid Id")

    def update(self):
        df = pd.read_csv(self.filename)

        command = input("What you want to update(Category/Amount/Date): ").lower()

        try:
            expense_id = int(input("enter the ID which is belongs: "))

            if expense_id not in df["ID"].values:
               print("ID not found.")
               return
    
            updated = False
    
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

        except ValueError:
            print("Its not the valid Id.")

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

            colors = ['#2b5c8f', '#4682b4', '#6baed6', '#b3cde3', '#fbb4ae']
            text_color = '#2c3e50'

            category_totals.plot(
               kind="pie", 
               autopct="%1.1f%%", 
               startangle=30, 
               figsize=(6, 6),
               colors=colors,
               textprops=dict(color=text_color, fontsize=11),
               pctdistance=0.75,
               wedgeprops=dict(width=0.4, edgecolor='black', linewidth=2.5)
            )

            plt.title("Expense Breakdown by Category",  fontsize=15, fontweight='bold', color=text_color, pad=20)
            plt.ylabel("") 

            for text in plt.gca().texts:
                if '%' in text.get_text():
                    text.set_weight('bold')
                    text.set_color('white')

            plt.tight_layout()        
            plt.show()

        elif visual_type == "bar":

            text_color = "#29296e"

            ax = category_totals.sort_values().plot(
                kind="barh", 
                color="#8b5cf6", 
                edgecolor="none",
                figsize=(10, 6)
                )

            plt.title("Total spending by category")
            plt.xlabel("Total Spent (₹)")
            plt.ylabel("Category")
            plt.grid(axis="x", linestyle="--", alpha=0.7)

            ax.grid(axis="x", linestyle="--", alpha=0.5, color='#e2e8f0')
            for spine in ["top", "right", "left"]:
                ax.spines[spine].set_visible(False)
 
            ax.tick_params(colors=text_color)
            plt.tight_layout()           
            plt.show()

        elif visual_type == "line":
      
            text_color = "#2c3e50"
            accent_green = "#0dcf8f"
        
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.dropna(subset=["Date"])
        
        
            df = df.sort_values("Date").copy()
            df = df.set_index("Date")
        
            monthly_trend = df["Amount"].resample("ME").sum()
        
            fig, ax = plt.subplots(figsize=(10, 5))
        
            ax.plot(
                monthly_trend.index,
                monthly_trend.values,
                marker="o",
                markersize=6,
                color=accent_green,
                linewidth=3,
                markeredgecolor="white",
                markeredgewidth=2
            )
        
            ax.fill_between(
                monthly_trend.index,
                monthly_trend.values,
                color=accent_green,
                alpha=1
            )
        
            ax.set_title(
                "Monthly Expense Trend",
                fontsize=15,
                fontweight="bold",
                color=text_color,
                pad=15
            )
        
            ax.set_xlabel("Month", color=text_color, labelpad=10)
            ax.set_ylabel("Total Spent (₹)", color=text_color, labelpad=10)
        
            ax.grid(True, linestyle="--", alpha=0.3, color="#94a3b8")
        
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        
            ax.tick_params(colors=text_color)
        
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f"₹{x:,.0f}")
            )
        
            fig.autofmt_xdate()
            fig.tight_layout()
            plt.show()

        else:
            print("Invalid visual type. Choose Pie, Bar, or Line.")
                  
      
user_1 = ExpenseTracker("Expense")
user_1.update()