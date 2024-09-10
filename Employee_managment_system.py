import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
#For export to excel
import pandas as pd


font1=('Arial', 16, 'bold')

entry_id_time=None
entry_entry_time=None
entry_exit_time=None

def add_employee():
    employee_id=entry_id.get()
    employee_name=entry_name.get()
    employee_role=entry_role.get()
    employee_gender=entry_gender.get()

    con=sqlite3.connect('Employees.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Employees(id INTEGER PRIMARY KEY, name TEXT, role TEXT, gender TEXT)")
    cur.execute("INSERT INTO Employees VALUES(?, ?, ?, ?)", (employee_id, employee_name, employee_role, employee_gender))
    con.commit()
    con.close()

    messagebox.showinfo("Success", "Employee added successfully")

def save_time():

    global entry_id_time, entry_entry_time, entry_exit_time

    employee_id = entry_id_time.get()
    entry_save_time= entry_entry_time.get()
    exit_save_time= entry_exit_time.get()

    entry_datetime=datetime.strptime(entry_save_time, "%H:%M")
    exit_datetime=datetime.strptime(exit_save_time, "%H:%M")
    performance_seconds=(exit_datetime-entry_datetime).total_seconds()
    performance_hours = int(performance_seconds//3600)
    performance_minutes = int((performance_seconds % 3600)//60)
    performance_daily = f"{performance_hours}h {performance_minutes}m"

    con = sqlite3.connect('Employees.db')
    cur = con.cursor()
    cur.execute('SELECT id FROM Employees WHERE id=?', (employee_id,))
    employee = cur.fetchone()
    con.close()

    if not employee:
        messagebox.showerror("Error", "Employee ID does not exist.")

    else:
        con = sqlite3.connect('Employees.db')
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS SaveTimeEmployee(employee_id INTEGER, entry_time TEXT, exit_time TEXT, performance_daily REAL, FOREIGN KEY(employee_id)REFERENCES Employees(id))')
        cur.execute('INSERT INTO SaveTimeEmployee VALUES(?, ?, ?, ?)',
                    (employee_id, entry_save_time, exit_save_time, performance_daily))

        con.commit()
        con.close()

        messagebox.showinfo("Success", "Time saved successfully.")

def time_window():
    global entry_id_time, entry_entry_time, entry_exit_time

    time_win=tk.Tk()
    time_win.title('Time Employee')
    time_win.config(bg='#161C25')
    time_win.geometry('400x500')
    time_win.resizable(False, False)

    label_id_time=tk.Label(time_win, text='ID:', bg='#161C25', fg='#fff', font=font1)
    label_id_time.grid(row=0, column=0, padx=10, pady=10)

    entry_id_time = tk.Entry(time_win, borderwidth=1, font=font1, width=20)
    entry_id_time.grid(row=0, column=1, padx=10, pady=10)

    label_entry_time = tk.Label(time_win, text='Entry:', bg='#161C25', fg='#fff', font=font1)
    label_entry_time.grid(row=1, column=0, padx=10, pady=10)

    entry_entry_time = tk.Entry(time_win, borderwidth=1, font=font1, width=20)
    entry_entry_time.grid(row=1, column=1, padx=10, pady=10)

    label_exit_time = tk.Label(time_win, text='Exit:', bg='#161C25', fg='#fff', font=font1)
    label_exit_time.grid(row=2, column=0, padx=10, pady=10)

    entry_exit_time = tk.Entry(time_win, borderwidth=1, font=font1, width=20)
    entry_exit_time.grid(row=2, column=1, padx=10, pady=10)

    button_save_time=tk.Button(time_win, command=save_time, text='Save Time', font=font1, bg='#ff0000', fg='#fff')
    button_save_time.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    time_win.mainloop()

def show_database():
    db_win = tk.Tk()
    db_win.title('Database Viewer')
    db_win.geometry('800x400')

    notebook = ttk.Notebook(db_win)
    notebook.pack(pady=10, expand=True)

    frame1 = ttk.Frame(notebook, width=800, height=400)
    frame2 = ttk.Frame(notebook, width=800, height=400)
    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)

    notebook.add(frame1, text='Employees')
    notebook.add(frame2, text='Time Entries')

    tree1 = ttk.Treeview(frame1, columns=('ID', 'Name', 'Role', 'Gender'), show='headings')
    tree1.heading('ID', text='ID')
    tree1.heading('Name', text='Name')
    tree1.heading('Role', text='Role')
    tree1.heading('Gender', text='Gender')
    tree1.pack(fill='both', expand=True)

    tree2 = ttk.Treeview(frame2, columns=('Employee ID', 'Entry Time', 'Exit Time', 'Performance Daily'), show='headings')
    tree2.heading('Employee ID', text='Employee ID')
    tree2.heading('Entry Time', text='Entry Time')
    tree2.heading('Exit Time', text='Exit Time')
    tree2.heading('Performance Daily', text='Performance Daily')
    tree2.pack(fill='both', expand=True)

    con = sqlite3.connect('Employees.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM Employees')
    employee = cur.fetchall()
    for emp in employee:
        tree1.insert('', 'end', values=emp)

    cur.execute('SELECT * FROM saveTimeEmployee')
    time_entry = cur.fetchall()
    for entry in time_entry:
        tree2.insert('', 'end', values=entry)

    con.close()
    db_win.mainloop()

def export_to_excel():
    con = sqlite3.connect('Employees.db')
    
    # خواندن جدول Employees
    df_employees = pd.read_sql_query("SELECT * FROM Employees", con)
    
    # خواندن جدول SaveTimeEmployee
    df_time = pd.read_sql_query("SELECT * FROM SaveTimeEmployee", con)
    
    con.close()
    
    # ذخیره اطلاعات به فایل اکسل
    with pd.ExcelWriter('EmployeesData.xlsx') as writer:
        df_employees.to_excel(writer, sheet_name='Employees', index=False)
        df_time.to_excel(writer, sheet_name='Time Entries', index=False)


root = tk.Tk()
root.title('Employee Managment')
root.config(bg='#161C25')
root.geometry('400x500')
root.resizable(False,False)

label_id = tk.Label(root, text='ID:', bg='#161C25', fg='#fff', font=font1)
label_id.grid(row=0, column=0, padx=10, pady=10)

entry_id = tk.Entry(root, borderwidth=1, font=font1, width=20)
entry_id.grid(row=0, column=1, padx=10, pady=10)

label_name = tk.Label(root, text='Name:', bg='#161C25', fg='#fff', font=font1)
label_name.grid(row=1, column=0, padx=10, pady=10)

entry_name = tk.Entry(root, borderwidth=1, font=font1, width=20)
entry_name.grid(row=1, column=1, padx=10, pady=10)

label_role = tk.Label(root, text='Role:', bg='#161C25', fg='#fff', font=font1)
label_role.grid(row=2, column=0, padx=10, pady=10)

entry_role = tk.Entry(root, borderwidth=1, font=font1, width=20)
entry_role.grid(row=2, column=1, padx=10, pady=10)

label_gender = tk.Label(root, text='Gender:', bg='#161C25', fg='#fff', font=font1)
label_gender.grid(row=3, column=0, padx=10, pady=10)

entry_gender = tk.Entry(root, borderwidth=1, font=font1, width=20)
entry_gender.grid(row=3, column=1, padx=10, pady=10)

button_add= tk.Button(root, command=add_employee, text='Add Employee', font=font1, bg='#ff0000', fg='#fff')
button_add.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

button_time= tk.Button(root, command=time_window, text='Time Employee', font=font1, bg='#ff0000', fg='#fff')
button_time.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

button_show_db = tk.Button(root, command=show_database, text='Show Database', font=font1, bg='#ff0000', fg='#fff')
button_show_db.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

#اضافه کردن دکمه برای تبدیل خروجی به اکسل
button_export_excel = tk.Button(root, command=export_to_excel, text='Export to Excel', font=font1, bg='#ff0000', fg='#fff')
button_export_excel.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
