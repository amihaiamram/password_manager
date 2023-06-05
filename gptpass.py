import sqlite3
import time
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
    insert_query = "INSERT INTO passes VALUES (?, ?, ?)"
    date_now = time.ctime()
    conn.execute(insert_query, (site, passcode, date_now))

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def delete(site, conn):
    query = "DELETE FROM passes WHERE site = ?"
    conn.execute(query, (site,))
    print_rows(conn)

def print_rows(conn):
    query = "SELECT site, passcode, date FROM passes ORDER BY date"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()

    print("site, code, date")
    for row in rows:
        print(', '.join(row))

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    conn = create_connection()
    create_table(conn)

    while True:
        clear_screen()

        print("Password Manager")
        print("================")
        print("1. Add Password")
        print("2. Print Passwords")
        print("3. Change Password")
        print("4. Generate Password")
        print("5. Delete Password")
        print("6. Search Password")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            site = input("Enter the site: ")
            passcode = input("Enter the password: ")
            add(site, passcode, conn)
            print("Password added successfully!")

        elif choice == '2':
            print_rows(conn)

        elif choice == '3':
            site = input("Enter the site: ")
            old_pass = input("Enter the old password: ")
            new_pass = input("Enter the new password: ")
            update_passcode(new_pass, old_pass, site, conn)
            print("Password updated successfully!")

        elif choice == '4':
            site = input("Enter the site: ")
            length = int(input("Enter the desired length: "))
            password = generate_password(length)
            print("Generated Password:", password)
            save = input("Do you want to save the password? (y/n): ")
            if save.lower() == 'y':
                add(site, password, conn)
                print("Password saved successfully!")

        elif choice == '5':
            site = input("Enter the site: ")
            delete(site, conn)
            print("Password deleted successfully!")

        elif choice == '6':
            site = input("Enter the site: ")
            row = search(site, conn)
            if row:
                print("Site:", row[0])
                print("Password:", row[1])
                print("Date:", row[2])
            else:
                print("Password not found!")

        elif choice == '0':
            break

        input("Press Enter to continue...")

    conn.commit()
    conn.close()

    print("Goodbye!")

if __name__ == '__main__':
    main()
