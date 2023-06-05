import sqlite3
import time

import sqlite3
import random
import string
import os

def search(site, cur):
    query = "SELECT * FROM passes WHERE site = ?"
    cur.execute(query, (site,))
    row = cur.fetchone()
    return row


def change(n_pass, o_pass, cur, date,site):
    row = search(site, cur)
    passcode_to_update = f'{o_pass}'
    new_passcode = f'{n_pass}'

    update_query = "UPDATE passes SET passcode = ? WHERE passcode = ?"

    cur.execute(update_query, (new_passcode, passcode_to_update))


def add(site, passcode, date, cur):
    cur.execute("""
            INSERT INTO passes VALUES
                (?, ?, ?)        """, (site, passcode, date))


def make(site, date, cur):
    upletters = string.ascii_uppercase
    lowletters = string.ascii_lowercase
    symbols = string.punctuation
    size = int(input(" what is the desired length ? "))
    passw = ''
    for i in range(size):
        choice = random.randint(1, 4)
        if choice == 1:
            a = random.randint(1, 9)
        elif choice == 2:
            a = random.choice(upletters)
        elif choice == 3:
            a = random.choice(lowletters)
        elif choice == 4:
            a = ''.join(random.choice(symbols))
        passw = passw + str(a)

    print(passw)
    ans = str(input("do you want to save password? "))
    if ans == 'y':
        add(site, passw, date, cur)


def delete(site, cur):
    site_to_delete = f'{site}'
    delete_query = "DELETE FROM  passes WHERE site = ?"
    cur.execute(delete_query, (site_to_delete,))
    print_row(cur)





def print_row(cur):
    print("site,code,date")
    for row in cur.execute("SELECT site, passcode FROM passes ORDER BY date"):
        print(row)



conn = sqlite3.connect('passes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passes (site, passcode, date)''')
date_now = time.ctime()

run = True
while run:
    options = 0
    while options == 0 or options > 6:
        options = int(input("""
                    what action do you want to perform 
                    1.add password 
                    2.print password
                    3.change password
                    4.create password 
                    5.delete password
                    6.search password
                   """))
        # done
        if options in [1, 3, 4, 5, 6]:
            place = input("site: ")
            code = input("password: ")
            if options == 1:
                add(place, code, date_now, c)
            elif options == 4:
                make(place, date_now, c)
            elif options == 5:
                delete(place, c)
            elif options == 6:
                search(place, c)
            elif options == 3:
                new_pass, old_pass = input("Enter new password and old password: ").split()
                change(new_pass, old_pass, c, date_now, place)


        elif options == 2:
            print_row(c)

        conn.commit()

        choice = str(input(" do you wish to continue : y/n ")).lower()
        if choice == 'n':
            print("babye")
            run = False
        os.system('cls')

conn.close()
