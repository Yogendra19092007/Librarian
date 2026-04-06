import tkinter as tk
from tkinter import font
import backend

root = tk.Tk()
root.title("Librarian Dashboard")
root.geometry("520x420")
root.resizable(False, False)
root.configure(bg="#0b1120")

header_font = font.Font(family="Segoe UI", size=24, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Segoe UI", size=12, weight="bold")

header = tk.Label(root, text="Librarian Dashboard", fg="#f8fafc", bg="#0b1120", font=header_font)
header.pack(pady=(25, 10))

sub = tk.Label(root, text="Manage library inventory and member records", fg="#cbd5e1", bg="#0b1120", font=label_font)
sub.pack(pady=(0, 25))

card = tk.Frame(root, bg="#111827", bd=0, relief='ridge')
card.pack(padx=25, pady=10, fill='both', expand=True)

status = tk.Label(card, text=f"Total books: {len(backend.books)}   |   Total users: {len(backend.users)}", fg="#f8fafc", bg="#111827", font=label_font)
status.pack(pady=(20, 10))

button_frame = tk.Frame(card, bg="#111827")
button_frame.pack(pady=10)

button_style = {'bg': '#38bdf8', 'fg': '#0f172a', 'activebackground': '#0ea5e9', 'activeforeground': '#ffffff', 'bd': 0, 'font': button_font, 'width': 18, 'height': 2, 'cursor': 'hand2'}

def add_book():
    backend.add_book_dialog()
    refresh_status()


def remove_book():
    backend.remove_book_dialog()
    refresh_status()


def check():
    backend.show_all_books()


def user_history():
    backend.show_user_history()


def refresh_status():
    status.config(text=f"Total books: {len(backend.books)}   |   Total users: {len(backend.users)}")

add_btn = tk.Button(button_frame, text="Add Book", command=add_book, **button_style)
add_btn.grid(row=0, column=0, padx=10, pady=10)
remove_btn = tk.Button(button_frame, text="Remove Book", command=remove_book, **button_style)
remove_btn.grid(row=0, column=1, padx=10, pady=10)
check_btn = tk.Button(button_frame, text="View Books", command=check, **button_style)
check_btn.grid(row=1, column=0, padx=10, pady=10)
history_btn = tk.Button(button_frame, text="User History", command=user_history, **button_style)
history_btn.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()