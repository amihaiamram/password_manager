import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string
import os

DB_FILE = 'passes.db'

def create_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_table(conn):
    create_query = '''
        CREATE TABLE IF NOT EXISTS passes (
            site TEXT,
            passcode TEXT,
            date TEXT
        )
    '''
    conn.execute(create_query)

def search(site, conn):
    query = "SELECT * FROM passes WHERE site = ?"
    cur = conn.cursor()
    cur.execute(query, (site,))
    row = cur.fetchone()
    cur.close()
    return row

def update_passcode(new_pass, old_pass, site, conn):
    query = "UPDATE passes SET passcode = ? WHERE site = ? AND passcode = ?"
    conn.execute(query, (new_pass, site, old_pass))

def add(site, passcode, conn):
    insert_query = "INSERT INTO passes VALUES (?, ?, datetime('now'))"
    conn.execute(insert_query, (site, passcode))

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def delete(site, conn):
    query = "DELETE FROM passes WHERE site = ?"
    conn.execute(query, (site,))

def print_rows(conn):
    query = "SELECT site, passcode FROM passes ORDER BY date"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()

    output = "site, code, date\n"
    for row in rows:
        output += ', '.join(row) + "\n"

    return output

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def add_password():
    site = site_entry.get()
    passcode = passcode_entry.get()
    if site and passcode:
        conn = create_connection()
        create_table(conn)
        add(site, passcode, conn)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password added successfully!")
        site_entry.delete(0, tk.END)
        passcode_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both site and password!")

def clear_entries():
    site_entry.delete(0, tk.END)
    passcode_entry.delete(0, tk.END)

def generate_random_password():
    site = site_entry.get()
    length = int(length_entry.get())
    if site and length > 0:
        password = generate_password(length)
        passcode_entry.delete(0, tk.END)
        passcode_entry.insert(0, password)
    else:
        messagebox.showerror("Error", "Please enter site and desired length!")

def delete_password():
    site = site_entry.get()
    if site:
        conn = create_connection()
        delete(site, conn)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password deleted successfully!")
        site_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter the site!")

def search_password():
    site = site_entry.get()
    if site:
        conn = create_connection()
        row = search(site, conn)
        conn.close()
        if row:
            passcode_entry.delete(0, tk.END)
            passcode_entry.insert(0, row[1])
            messagebox.showinfo("Success", "Password found!")
        else:
            messagebox.showinfo("Not Found", "Password not found!")
    else:
        messagebox.showerror("Error", "Please enter the site!")

def print_all_passwords():
    conn = create_connection()
    output = print_rows(conn)
    conn.close()
    messagebox.showinfo("Passwords", output)

def main():
    global site_entry, passcode_entry, length_entry

    root = tk.Tk()
    root.title("Password Manager")

    site_label = tk.Label(root, text="Site:")
    site_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    site_entry = tk.Entry(root)
    site_entry.grid(row=0, column=1, padx=10, pady=5)

    passcode_label = tk.Label(root, text="Password:")
    passcode_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    passcode_entry = tk.Entry(root)
    passcode_entry.grid(row=1, column=1, padx=10, pady=5)

    length_label = tk.Label(root, text="Length:")
    length_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    length_entry = tk.Entry(root)
    length_entry.grid(row=2, column=1, padx=10, pady=5)

    add_button = tk.Button(root, text="Add Password", command=add_password)
    add_button.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    generate_button = tk.Button(root, text="Generate Password", command=generate_random_password)
    generate_button.grid(row=3, column=1, padx=10, pady=5)

    delete_button = tk.Button(root, text="Delete Password", command=delete_password)
    delete_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

    search_button = tk.Button(root, text="Search Password", command=search_password)
    search_button.grid(row=4, column=1, padx=10, pady=5)

    print_button = tk.Button(root, text="Print Passwords", command=print_all_passwords)
    print_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

    clear_button = tk.Button(root, text="Clear", command=clear_entries)
    clear_button.grid(row=5, column=1, padx=10, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
