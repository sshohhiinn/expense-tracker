# 📄 Project Documentation — Expense Tracker


## 1. Introduction

### 1.1 Purpose
The Expense Tracker is a Python-based application designed to help users record, manage, and analyze their daily expenses. It provides a simple and efficient way to track spending habits and export financial data.

### 1.2 Project Scope
The scope of this project is to design and develop an Expense Tracker application using Python that enables users to add, edit, delete, and filter expenses by category, date, and amount, featuring persistent CSV file storage, a Tkinter desktop GUI, and a Flask web application deployed on Vercel.

### 1.3 Intended Audience
- Students managing pocket money
- Individuals tracking personal finances
- Anyone who wants to monitor daily spending



## 2. System Overview

The Expense Tracker application is built in three versions:

| Version | Technology | Platform |
|---|---|---|
| CLI | Python | Terminal |
| Desktop GUI | Python + Tkinter | Windows/Mac/Linux |
| Web App | Python + Flask | Browser (Vercel) |



## 3. Features & Functionality

### 3.1 Add Expense
- Enter date (defaults to today)
- Select category from 8 options
- Enter description and amount
- Data saved automatically to CSV

### 3.2 View Expenses
- Display all expenses in a table
- Shows ID, Date, Category, Description, Amount
- Total amount shown at the bottom

### 3.3 Filter Expenses
- Filter by Category
- Filter by Month (YYYY-MM)
- Filter by Date (YYYY-MM-DD)
- Search by keyword

### 3.4 Edit Expense
- Select expense by ID
- Update any field
- Changes saved immediately

### 3.5 Delete Expense
- Delete by ID
- Delete all expenses option
- Confirmation before deletion

### 3.6 Summary & Statistics
- Total amount spent
- Monthly breakdown
- Category-wise breakdown with percentage
- Highest and lowest expense

### 3.7 Export CSV
- Export all or monthly expenses
- Saved as a downloadable CSV file



### 4.1 Data Model
```
expenses.csv
─────────────────────────────────────
ID | Date       | Category | Description | Amount
1  | 2025-06-01 | Food     | Lunch       | 150.00
2  | 2025-06-02 | Transport| Uber        | 220.00
```

### 4.2 Key Functions

| Function | Description |
|---|---|
| `init_file()` | Creates CSV file if not exists |
| `load_expenses()` | Reads all expenses from CSV |
| `save_expenses()` | Writes expenses to CSV |
| `next_id()` | Generates unique ID |
| `add_expense()` | Adds new expense record |
| `delete_expense()` | Removes expense by ID |
| `edit_expense()` | Updates existing expense |
| `view_expenses()` | Displays filtered expenses |
| `summary()` | Shows statistics |
| `export_csv()` | Exports data to CSV |

### 4.3 Flask API Routes

| Route | Method | Description |
|---|---|---|
| `/expenses` | GET | View all expenses |
| `/expenses/add` | POST | Add new expense |
| `/expenses/delete/<id>` | POST | Delete expense |
| `/expenses/edit/<id>` | POST | Edit expense |
| `/expenses/export` | GET | Download CSV |



## 5. Categories

```
Food | Transport | Shopping | Bills |
Health | Entertainment | Education | Other
```


## 6. Testing

| Test Case | Input | Expected Output | Result |
|---|---|---|---|
| Add expense | Valid amount & date | Expense saved to CSV | ✅ Pass |
| Add expense | Invalid amount (text) | Error message shown | ✅ Pass |
| Delete expense | Valid ID | Expense removed | ✅ Pass |
| Delete expense | Invalid ID | Not found message | ✅ Pass |
| Filter by category | "Food" | Only food expenses | ✅ Pass |
| Export CSV | Click export | CSV file downloaded | ✅ Pass |
| View summary | Any data | Stats displayed | ✅ Pass |



## 7. Limitations

- Data stored locally in CSV (not cloud database)
- No user authentication
- No multi-currency support (only ₹)
- No graphical charts (text-based summary)


## 8. Future Enhancements

- 📊 Visual charts using Matplotlib
- 💱 Multi-currency support
- 🔔 Monthly budget alerts
- 👥 Multi-user login system
- ☁️ Cloud database (SQLite/PostgreSQL)
- 📱 Mobile app version



## 9. Conclusion

The Expense Tracker application successfully delivers a complete personal finance management solution. It demonstrates Python file handling, GUI development, web development, and data management skills developed during the CodeTech IT Solutions internship.


