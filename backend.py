# backend.py

import sqlite3
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('librarian.db')
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    quantity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    lib_id TEXT PRIMARY KEY,
    borrowed TEXT,  -- JSON string for list
    history TEXT    -- JSON string for list
)
''')

conn.commit()

# Insert initial data if tables are empty
cursor.execute('SELECT COUNT(*) FROM books')
if cursor.fetchone()[0] == 0:
    cursor.executemany('INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)',
                       [
                           (1, "Python Basics", "Guido van Rossum", 5),
                           (2, "AI for Everyone", "Andrew Ng", 4),
                           (3, "Data Structures", "Robert Lafore", 3),
                           (4, "Web Development", "Jon Duckett", 6),
                           (5, "Machine Learning", "Tom Mitchell", 2),
                           (6, "Database Systems", "Ramez Elmasri", 4),
                           (7, "Operating Systems", "Abraham Silberschatz", 3),
                           (8, "Computer Networks", "Andrew S. Tanenbaum", 5),
                           (9, "Discrete Mathematics", "Kenneth Rosen", 3),
                           (10, "Algorithms", "Cormen", 4),
                           (11, "Python Advanced", "Jake VanderPlas", 5),
                           (12, "Introduction to AI", "Stuart Russell", 2),
                           (13, "Software Engineering", "Ian Sommerville", 3),
                           (14, "Cyber Security", "William Stallings", 4),
                           (15, "Cloud Computing", "Rajkumar Buyya", 2),
                           (16, "Mobile App Dev", "Reto Meier", 3),
                           (17, "Digital Logic", "M. Morris Mano", 4),
                           (18, "Artificial Intelligence", "Elaine Rich", 3),
                           (19, "Java Programming", "Herbert Schildt", 5),
                           (20, "Network Security", "Charlie Kaufman", 2)
                       ])
    conn.commit()

cursor.execute('SELECT COUNT(*) FROM users')
if cursor.fetchone()[0] == 0:
    cursor.executemany('INSERT INTO users (lib_id, borrowed, history) VALUES (?, ?, ?)',
                       [
                           (f"U{100+i}", "[]", "[]") for i in range(1, 21)
                       ])
    conn.commit()

# LIST OF DICTIONARIES (MAIN STORAGE) - loaded from DB
books = []
users = []
current_user = None

def load_books():
    global books
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    books = [{"id": row[0], "title": row[1], "author": row[2], "quantity": row[3]} for row in rows]

def load_users():
    global users
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    users = [{"lib_id": row[0], "borrowed": json.loads(row[1]) if row[1] else [], "history": json.loads(row[2]) if row[2] else []} for row in rows]

def save_books():
    cursor.execute('DELETE FROM books')
    for book in books:
        cursor.execute('INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)',
                       (book["id"], book["title"], book["author"], book["quantity"]))
    conn.commit()

def save_users():
    cursor.execute('DELETE FROM users')
    for user in users:
        cursor.execute('INSERT INTO users (lib_id, borrowed, history) VALUES (?, ?, ?)',
                       (user["lib_id"], json.dumps(user["borrowed"]), json.dumps(user["history"])))
    conn.commit()

# Load data on startup
load_books()
load_users()


# 🔐 LOGIN
def validate_user(lib_id):
    global current_user
    for user in users:
        if user["lib_id"] == lib_id:
            current_user = user
            return True
    return False


# 📚 ADD BOOK
def add_book(book_id, title, author, quantity):
    books.append({
        "id": book_id,
        "title": title,
        "author": author,
        "quantity": quantity
    })
    save_books()


# ❌ REMOVE BOOK
def remove_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    save_books()


# 🔍 FIND BOOK
def find_book(name):
    for book in books:
        if book["title"].lower() == name.lower():
            return book
    return None


# 📥 ISSUE BOOK
def issue_book(name):
    book = find_book(name)

    if book:
        if book["quantity"] > 0:
            book["quantity"] -= 1
            current_user["borrowed"].append(book["title"])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_user["history"].append(f"{timestamp} - Borrowed: {book['title']}")
            save_books()
            save_users()
            return "Book Issued"
        else:
            return "Not Available"
    return "Book Not Found"


# 📤 RETURN BOOK
def return_book(name):
    book = find_book(name)

    if book and name in current_user["borrowed"]:
        book["quantity"] += 1
        current_user["borrowed"].remove(name)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_user["history"].append(f"{timestamp} - Returned: {name}")
        save_books()
        save_users()
        return "Book Returned"
    return "Invalid Return"


# 📊 CHECK AVAILABILITY
def check_availability(name):
    book = find_book(name)
    if book:
        return f"Available: {book['quantity']}"
    return "Book Not Found"


# 📋 GET ALL BOOKS
def get_books():
    return books


# 📜 USER HISTORY
def get_user_history():
    return current_user["history"] if current_user else []

# GUI helpers for tkinter

def _create_tk_root():
    root = tk.Tk()
    root.withdraw()
    return root


def add_book_dialog():
    root = _create_tk_root()
    try:
        book_id = simpledialog.askinteger("Add Book", "Book ID:", parent=root)
        if book_id is None:
            return
        title = simpledialog.askstring("Add Book", "Book Title:", parent=root)
        if not title:
            return
        author = simpledialog.askstring("Add Book", "Author:", parent=root)
        if not author:
            return
        quantity = simpledialog.askinteger("Add Book", "Quantity:", parent=root, minvalue=1)
        if quantity is None:
            return
        add_book(book_id, title, author, quantity)
        messagebox.showinfo("Success", "Book added successfully", parent=root)
    finally:
        root.destroy()


def remove_book_dialog():
    root = _create_tk_root()
    try:
        book_id = simpledialog.askinteger("Remove Book", "Book ID:", parent=root)
        if book_id is None:
            return
        remove_book(book_id)
        messagebox.showinfo("Success", "Book removed successfully", parent=root)
    finally:
        root.destroy()


def show_all_books():
    root = _create_tk_root()
    try:
        if not books:
            messagebox.showinfo("Books", "No books available.", parent=root)
            return
        book_lines = [f"{book['id']}: {book['title']} by {book['author']} (qty: {book['quantity']})" for book in books]
        messagebox.showinfo("Books", "\n".join(book_lines), parent=root)
    finally:
        root.destroy()


def open_borrow_dialog():
    root = _create_tk_root()
    try:
        available_books = [book['title'] for book in books if book['quantity'] > 0]
        if not available_books:
            messagebox.showinfo("Borrow Book", "No books are currently available to borrow.", parent=root)
            return

        top = tk.Toplevel(root)
        top.title("Borrow Book")
        top.geometry("350x180")

        tk.Label(top, text="Select a book to borrow:").pack(pady=(15, 10))
        selected_book = tk.StringVar(value=available_books[0])
        tk.OptionMenu(top, selected_book, *available_books).pack(pady=5)

        def borrow_action():
            name = selected_book.get()
            result = issue_book(name)
            messagebox.showinfo("Borrow Book", result, parent=top)
            top.destroy()

        tk.Button(top, text="Borrow", command=borrow_action, width=15).pack(pady=15)
        top.grab_set()
        top.wait_window()
    finally:
        root.destroy()


def open_return_dialog():
    root = _create_tk_root()
    try:
        if not current_user or not current_user.get('borrowed'):
            messagebox.showinfo("Return Book", "You have no borrowed books to return.", parent=root)
            return

        top = tk.Toplevel(root)
        top.title("Return Book")
        top.geometry("350x180")

        tk.Label(top, text="Select a book to return:").pack(pady=(15, 10))
        selected_book = tk.StringVar(value=current_user['borrowed'][0])
        tk.OptionMenu(top, selected_book, *current_user['borrowed']).pack(pady=5)

        def return_action():
            name = selected_book.get()
            result = return_book(name)
            messagebox.showinfo("Return Book", result, parent=top)
            top.destroy()

        tk.Button(top, text="Return", command=return_action, width=15).pack(pady=15)
        top.grab_set()
        top.wait_window()
    finally:
        root.destroy()


def open_check_dialog():
    root = _create_tk_root()
    try:
        name = simpledialog.askstring("Check Availability", "Book Title:", parent=root)
        if not name:
            return
        result = check_availability(name)
        messagebox.showinfo("Check Availability", result, parent=root)
    finally:
        root.destroy()


def show_user_history():
    root = _create_tk_root()
    try:
        if not current_user:
            messagebox.showerror("Error", "No user is logged in.", parent=root)
            return
        history = current_user.get("history", [])
        if not history:
            messagebox.showinfo("History", "No history available.", parent=root)
            return
        messagebox.showinfo("History", "\n".join(history), parent=root)
    finally:
        root.destroy()