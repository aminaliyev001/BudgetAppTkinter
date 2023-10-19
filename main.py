from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style
from tkinter import Text
from PIL import Image, ImageTk

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 450
root = tk.Tk()
style = Style(theme='cosmo')
style.configure('Large.TButton', font=('Arial', 16, 'bold'))
style.configure('Lightgrey.TFrame', background='lightgrey')
style.configure('Red.TButton', background='red', foreground='white', font=('Arial', 16), borderwidth=0, relief='flat')
style.configure('Grey.TButton', background='grey', foreground='white', font=('Arial', 16), borderwidth=0, relief='flat')
style.configure('Blue.TFrame', background='#4995eb')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (WINDOW_WIDTH/2)
y = (screen_height/2) - (WINDOW_HEIGHT/2)
root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
expenses = []
users = []
notes = []
budget = 0

edit_icon = tk.PhotoImage(file='pen.png')
delete_icon = tk.PhotoImage(file='correct.png')

def update_notes_display():
    global notes_frame
    for widget in notes_frame.winfo_children():
        widget.destroy()
    grid_frame = ttk.Frame(notes_frame)
    grid_frame.pack(pady=20)

    style.configure('White.TButton', background="white", borderwidth=0, relief="flat")
    if not notes:
        note_label = ttk.Label(grid_frame, text="Empty", font=("Arial", 17))
        note_label.grid(sticky=tk.W, padx=20, pady=5)
        return

    for idx, note in enumerate(notes):
        row = idx // 2
        col = (idx % 2) * 3 

        note_label = ttk.Label(grid_frame, text="\u2022 " + note['text'], font=("Arial", 17))
        note_label.grid(row=row, column=col, sticky=tk.W, padx=20, pady=5)

        edit_button = ttk.Button(grid_frame, image=edit_icon,style="White.TButton", command=lambda note_id=note['id']: edit_note(note_id, notes_frame))
        edit_button.grid(row=row, column=col+1)

        delete_button = ttk.Button(grid_frame, image=delete_icon,style="White.TButton", command=lambda note_id=note['id']: delete_note(note_id, notes_frame))
        delete_button.grid(row=row, column=col+2)

def edit_note(idx, frame):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Note")

    window_width, window_height = 1000, 300
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    
    edit_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    lbl_header = ttk.Label(edit_window, text="Edit a note", font=("Arial", 30))
    lbl_header.pack(pady=20,anchor="center")

    lbl_name = ttk.Label(edit_window, text="Text")
    lbl_name.pack(pady=20, anchor="center")

    entry = ttk.Entry(edit_window)
    entry.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    note_text = next((note['text'] for note in notes if note['id'] == idx), '')
    entry.insert(0, note_text)

    submit_button = ttk.Button(edit_window, text="Save", command=lambda: save_edit(idx, entry.get(), frame, edit_window))
    submit_button.pack(pady=20)

def save_edit(note_id, entry,frame,window):
    global notes
    for note in notes:
        if note['id'] == note_id:
            note['text'] = entry
            break
    window.destroy()
    save_to_json_file()
    update_notes_display()

def delete_note(note_id, frame):
    global notes
    notes = [note for note in notes if note['id'] != note_id]
    update_notes_display()
    save_to_json_file()


def load_from_json_file():
    global expenses, users, notes,budget
    with open("data.json", "r") as file:
        data = json.load(file)
        expenses = data.get("expenses", [])
        users = data.get("users", [])
        notes = data.get("notes", [])
        budget = data.get("budget", 0)

def generate_id(entity_list, prefix):
    if entity_list:
        last_id = entity_list[-1]['id']
        new_id_num = int(last_id[1:]) + 1
        return f"{prefix}{new_id_num:03}"
    else:
        return f"{prefix}001"
    
def save_to_json_file():
    global expenses, users, notes,budget
    data = {
        "expenses": expenses,
        "users": users,
        "notes": notes,
        "budget":budget
    }
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def update_sum():
    global total_label, remaining_label, budget_label, budget
    total = sum(float(expense["Price"]) for expense in expenses)
    remaining = budget - total
    total_label.config(text=f"Total: {total:.2f}$")
    remaining_label.config(text=f"Remaining: {remaining:.2f}$")
    budget_label.config(text=f"Budget: {budget:.2f}$")


def save_note(entry,root,window):
    global notes
    if not entry.strip():
        messagebox.showwarning("Warning", "Please enter a valid note.")
        return
    new_id = generate_id(notes,"N")
    notes.append({"id": new_id, "text": entry})
    save_to_json_file()
    window.destroy()
    update_notes_display()

def add_note(root):
    edit_window = tk.Toplevel(root)
    edit_window.title("Add Note")

    window_width, window_height = 1000, 300
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    
    edit_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    lbl_header = ttk.Label(edit_window, text="Add a note", font=("Arial", 30))
    lbl_header.pack(pady=20,anchor="center")

    lbl_name = ttk.Label(edit_window, text="Text")
    lbl_name.pack(pady=20, anchor="center")

    entry = ttk.Entry(edit_window)
    entry.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    submit_button = ttk.Button(edit_window, text="Save", command=lambda: save_note(entry.get(), root, edit_window))
    submit_button.pack(pady=20)
    
def login_func():
    global username_entry,password_entry
    username = username_entry.get()
    password = password_entry.get()
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                messagebox.showinfo("Success", "Logged in successfully")
                main_page()
                return
            else:
                messagebox.showerror("Error", "Invalid password. Try again please")
        else:
            messagebox.showerror("Error", "Invalid username. Try again please")
def logout():
    for widget in root.winfo_children():
        widget.destroy()
    x = (screen_width/2) - (WINDOW_WIDTH/2)
    y = (screen_height/2) - (WINDOW_HEIGHT/2)
    root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
    login_page()
def main_page():
    global tree, total_label, notes_frame,remaining_label,budget_label
    x = (screen_width/2) - (1200/2)
    y = (screen_height/2) - (750/2)
    root.geometry('%dx%d+%d+%d' % (1200, 750, x, y))
    style.configure('Treeview.Heading', background='lightgrey')
    for widget in root.winfo_children():
        widget.destroy() 

    header_label = ttk.Label(root, text="Expenses", font=("Arial", 24))
    header_label.pack(pady=20)

    columns = ("Date", "Name", "Description", "Price")
    tree_frame = ttk.Frame(root)
    tree_frame.pack(pady=10, padx=50, fill=tk.X)

    columns = ("Date", "Name", "Description", "Price")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

    tree.column("Date", anchor=tk.CENTER, width=100)
    tree.column("Name", anchor=tk.CENTER, width=100)
    tree.column("Description", anchor=tk.CENTER, width=400)
    tree.column("Price", anchor=tk.CENTER, width=50)
    
    tree.heading("Date", text="Date")
    tree.heading("Name", text="Name")
    tree.heading("Description", text="Description")
    tree.heading("Price", text="Price")

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(pady=10, padx=50, expand=True, fill=tk.BOTH)
    summary_frame = ttk.Frame(tree_frame, style='Lightgrey.TFrame')
    summary_frame.pack(fill=tk.X, padx=50, pady=10)

    total_label = ttk.Label(summary_frame, font=('Arial', 16), background='lightgrey', foreground="#4995eb")
    total_label.grid(row=0, column=0, padx=20)

    remaining_label = ttk.Label(summary_frame, font=('Arial', 16), background='lightgrey', foreground="#4995eb")
    remaining_label.grid(row=0, column=1, padx=20)

    budget_label = ttk.Label(summary_frame, font=('Arial', 16), background='lightgrey', foreground="#4995eb")
    budget_label.grid(row=0, column=2, padx=20)

    def set_budget_callback():
        def save_budget():
            global budget
            try:
                new_budget = float(entry.get())
                if new_budget < 0:
                    messagebox.showwarning("Warning", "Budget cannot be negative.")
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid budget amount.")
                return
            budget = new_budget
            save_to_json_file()
            edit_window.destroy()
            update_sum()
            
        edit_window = tk.Toplevel(root)
        edit_window.title("Set budget")

        window_width, window_height = 1000, 300
        position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
        position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
        
        edit_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        lbl_header = ttk.Label(edit_window, text="Set a budget", font=("Arial", 30))
        lbl_header.pack(pady=20,anchor="center")

        lbl_name = ttk.Label(edit_window, text="Budget")
        lbl_name.pack(pady=20, anchor="center")

        entry = ttk.Entry(edit_window)
        entry.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)
        entry.insert(0, budget)
        submit_button = ttk.Button(edit_window, text="Save", command=save_budget)
        submit_button.pack(pady=20)
    
    set_budget_button = ttk.Button(summary_frame, text="Set Budget", command=set_budget_callback)
    set_budget_button.grid(row=0, column=3, padx=70)

    if expenses:
        for expense in expenses:
            tree.insert("", "end", values=(expense["Date"], expense["Name"], expense["Description"], expense["Price"]),tags=expense['id'])

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20, padx=50)

    btn_add_expense = ttk.Button(button_frame, text="Add Expense", command=add_expense)
    btn_add_expense.grid(row=0, column=0, padx=20)

    btn_edit_expense = ttk.Button(button_frame, text="Edit Selected Expense" ,command=edit_expense)
    btn_edit_expense.grid(row=0, column=1, padx=20)

    btn_delete_expense = ttk.Button(button_frame, text="Delete Selected Expense", command=delete_expense)
    btn_delete_expense.grid(row=0, column=2, padx=20)

    line_frame = ttk.Frame(root, height=2, style="Lightgrey.TFrame")
    line_frame.pack(fill=tk.X, pady=10, padx=10)
    line_frame.pack_propagate(0)  

    notes_header = ttk.Label(root, text="Notes", font=("Arial", 24))
    notes_header.pack(pady=10)

    add_button = ttk.Button(root, text="Add",command=lambda:add_note(root))
    add_button.pack(anchor='e', padx=10, pady=10)

    notes_frame = ttk.Frame(root)
    notes_frame.pack(pady=0, padx=100, fill=tk.X)

    logout_button = ttk.Button(root, text="Log Out", style='Red.TButton',command=logout)  
    logout_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  

    update_notes_display()
    update_sum()

def add_expense():
    expense_window = tk.Toplevel(root)
    
    window_width, window_height = 1000, 500
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    
    expense_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    expense_window.title("Add Expense")

    lbl_header = ttk.Label(expense_window, text="Add an expense", font=("Arial", 30))
    lbl_header.pack(pady=20,anchor="center")

    lbl_name = ttk.Label(expense_window, text="Name")
    lbl_name.pack(pady=20, anchor="center")
    
    entry_name = ttk.Entry(expense_window)
    entry_name.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    lbl_description = ttk.Label(expense_window, text="Description")
    lbl_description.pack(pady=5, anchor="center")
    
    entry_description = ttk.Entry(expense_window)
    entry_description.pack( anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    lbl_price = ttk.Label(expense_window, text="Price")
    lbl_price.pack(pady=5, anchor="center")
    
    entry_price = ttk.Entry(expense_window)
    entry_price.pack( anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    btn_save = ttk.Button(expense_window, text="Save Expense", command=lambda: save_new_expense(entry_name.get(), entry_description.get(), entry_price.get(),expense_window))
    btn_save.pack(pady=20, anchor="center")

def save_new_expense(name, description, price,expense_window):
    global tree, expenses
    if not name or not description or not price:
        messagebox.showerror("Error", "No field can be left empty")
        return
    try:
        float_price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Price should be a valid number")
        return
    current_date = datetime.now().strftime("%Y-%m-%d")
    newid = generate_id(expenses,"E")
    expenses.append({"id":newid,"Date": current_date, "Name": name, "Description": description, "Price": price})
    tree.insert("", tk.END, values=(current_date, name, description, price),tags=newid)
    save_to_json_file()
    messagebox.showinfo("Success","Successfully added the expense")
    expense_window.destroy()
    update_sum()

def edit_expense():
    selected_item = tree.selection()[0]  
    def submit():
        date = datetime.now().strftime("%Y-%m-%d")
        name = entry_name.get()
        description = entry_description.get()
        price = entry_price.get()
        if not name or not description or not price:
            messagebox.showerror("Error", "No field can be left empty")
            return
        try:
            float_price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price should be a valid number")
            return
        tree.item(selected_item, values=(date, name, description, price))
        selected_id = tree.item(selected_item, "tags")[0]
        for expense in expenses:
            if expense["id"] == selected_id:
                expense.update({"Date": date, "Name": name, "Description": description, "Price": price})
                break
        expense_window.destroy()
        update_sum()
        save_to_json_file()

    current_values = tree.item(selected_item, "values")
    expense_window = tk.Toplevel(root)
    window_width, window_height = 1000, 500
    position_x = root.winfo_x() + (root.winfo_width() // 2) - (window_width // 2)
    position_y = root.winfo_y() + (root.winfo_height() // 2) - (window_height // 2)
    
    expense_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    expense_window.title("Edit Expense")

    lbl_header = ttk.Label(expense_window, text="Edit an expense", font=("Arial", 30))
    lbl_header.pack(pady=20,anchor="center")

    lbl_name = ttk.Label(expense_window, text="Name")
    lbl_name.pack(pady=20, anchor="center")
    
    entry_name = ttk.Entry(expense_window)
    entry_name.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    lbl_description = ttk.Label(expense_window, text="Description")
    lbl_description.pack(pady=5, anchor="center")
    
    entry_description = ttk.Entry(expense_window)
    entry_description.pack(anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    lbl_price = ttk.Label(expense_window, text="Price")
    lbl_price.pack(pady=5, anchor="center")
    
    entry_price = ttk.Entry(expense_window)
    entry_price.pack( anchor="center",pady=5, padx=200, ipady=5, fill=tk.X)

    btn_save = ttk.Button(expense_window, text="Save Expense", command=submit)
    btn_save.pack(pady=20, anchor="center")

    entry_name.insert(0, current_values[1])
    entry_description.insert(0, current_values[2])
    entry_price.insert(0, current_values[3])

def delete_expense():
    selected_item = tree.selection()[0]
    selected_id = tree.item(selected_item, "tags")[0]
    tree.delete(selected_item)
    for expense in expenses:
        if expense["id"] == selected_id:
            expenses.remove(expense)
            break
    save_to_json_file()
    update_sum()
def login_page():
    global username_entry,password_entry
    lbl_title = ttk.Label(root, text="Login to Budget Planner", font=("Arial", 24))
    lbl_title.pack(pady=50)

    lbl_username = ttk.Label(root, text="Username",font=("Arial",17))
    lbl_username.pack(pady=5)
    username_entry = ttk.Entry(root)
    username_entry.pack(pady=5, padx=200, ipady=5, fill=tk.X)

    lbl_password = ttk.Label(root, text="Password",font=("Arial",17))
    lbl_password.pack(pady=5)
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=5, padx=200, ipady=5, fill=tk.X)

    btn_login = ttk.Button(root, text="Login", command=login_func,style="Large.TButton")
    btn_login.pack(pady=20, padx=350, ipady=5, fill=tk.X)

login_page()
load_from_json_file()
root.mainloop()