#!/usr/bin/env python3
import sys, getopt
import sqlite3
import csv
import os

def printErrBanner():
    print('level3.py -n <name> -a <age> -p <phone>')
    sys.exit(2)
    
def main(argv):
    name = ''
    age = ''
    phone = ''
    try:
        opts, args = getopt.getopt(argv,"hn:a:p:",["name=","age=","phone="])
    except getopt.GetoptError:
        printErrBanner()

    for opt, arg in opts:
        if opt == '-h':
            printErrBanner()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-a", "--age"):
            age = arg
        elif opt in ("-p", "--phone"):
            phone = arg
    return name, age, phone

class DbInterface:
    def __init__(self, name='database.db'):
        dbExists = False
        self.cursor = None
        self.usefulCmds = {
        'createTable':'''CREATE TABLE users (name text primary key, 
                                             age integer not null, 
                                             phone text not null,
                                             unique(name));''',
        'doesTableExist':'''SELECT count(name) 
                            FROM sqlite_master 
                            WHERE type='table' AND name='users' ''',
        'addUser':"INSERT INTO users VALUES (?,?,?)",
        'selectAll':'SELECT * FROM users ORDER BY name',
        'deleteUser':"DELETE FROM users WHERE name = ?",
        'updateUser':"UPDATE users SET name = ?, age = ?, phone = ? where name = ?",
        'clearAllUser':"DELETE FROM users"
        }
        self.open(name)

    def execute(self, cmd, args=None):
        if args:
            retval = self.cursor.execute(cmd, args)
        else:
            retval = self.cursor.execute(cmd)
        self.conn.commit()
        return retval

    def open(self, name):
        dbExists = False
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        if (not self.doesTableExist()):
            self.execute(self.usefulCmds['createTable'])

    def doesTableExist(self):
        retval = False
        self.cursor.execute(self.usefulCmds['doesTableExist'])
        if (self.cursor.fetchone()[0] == 1): 
            retval = True
        return retval

    def add(self, name, age, phone):
        try:
            self.execute(self.usefulCmds['addUser'], [name, age, phone])
        except sqlite3.IntegrityError:
            print("")
            print("!"*80)
            print("! Sorry, user already exists!")
            print("!"*80)
            print("")

    def dump(self):
        for row in self.execute(self.usefulCmds['selectAll']):
                print(row)

    def remove(self, name):
        try:
            self.execute(self.usefulCmds['deleteUser'], [name])
        except sqlite3.OperationalError:
            print("[Error] Could not find user to delete")

    def update(self, oldName, name, age, phone):
        self.execute(self.usefulCmds['updateUser'], [name, age, phone, oldName])

    def clearAll(self):
        self.execute(self.usefulCmds['clearAllUser'])

    def export(self, fileName='dbDump.csv'):
        self.execute(self.usefulCmds['selectAll'])
        results = self.cursor.fetchall()
        headers = [i[0] for i in self.cursor.description]

        csvFile = csv.writer(open(fileName, 'w', newline=''),
        delimiter=',', lineterminator='\r\n',
        quoting=csv.QUOTE_ALL, escapechar='\\')
        csvFile.writerow(headers)
        csvFile.writerows(results)
        print("Data export successful.")

    def close(self):
        self.conn.close()

class UserInterface:
    def __init__(self, name='', age=0, phone=''):
        self.name = name
        self.age = age
        self.phone = phone
        self.db = DbInterface("database.db")
        '''
        if len(name) is 0 or len(age) is 0:
            print("Must enter a name and age")
            exit(1)
        '''

    def check_input(self, prompt, is_string=True):
        retval = input(prompt)

        if is_string:
            try:
                retval = str(retval)
            except ValueError:
                print("Thats not a string!")
                exit(1)
        else:
            try:
                retval = int(retval)
            except ValueError:
                print("Tricksie hobbits, age is a number, not a construct")
                exit(1)
        return retval

    def add(self):
        print("Called add...")
        name = self.check_input("Name: ")
        age = self.check_input("Age: ", True)
        phone = self.check_input("Phone: ")
        self.db.add(name, age, phone)

    def remove(self):
        print("Called remove...")
        name = str(input("Name: "))
        self.db.remove(name)

    def edit(self):
        print("Called edit...")
        oldName = self.check_input("old name: ")
        name = self.check_input("new name: ")
        age = self.check_input("new age: ", True)
        phone = self.check_input("new phone: ")

        # TODO: Do we want to ignore values that users skip?
        self.db.update(oldName, name, age, phone)
        pass

    def clear(self):
        self.db.clearAll()
        print("Cleared all entries")

    def printAll(self):
        self.db.dump()

    def quit(self):
        print("Called quit")
        self.db.close()
        exit()

    def export(self):
        self.db.export()

    def process(self, arg):
        if arg == 0:
            self.quit()
        elif arg == 1:
            self.add()
        elif arg == 2:
            self.remove()
        elif arg == 3:
            self.edit()
        elif arg == 4:
            self.printAll()
        elif arg == 5:
            self.export()
        elif arg == 6:
            self.clear()
        else:
            print('Please do something else')
            print('')

    def printBanner(self):
        print('='*80)
        print("Select one of the following options:")
        print('-'*80)
        print("0. Quit")
        print("1. Add")
        print("2. Remove")
        print("3. Edit")
        print("4. Dump")
        print("5. Export")
        print("6. Clear all")
        print('='*80)

if __name__ == "__main__":
    #name, age, phone = main(sys.argv[1:])
    interface = UserInterface()

    while(1):
        interface.printBanner()
        userInput = input('==> ')
        try:
            userInput = int(userInput)
        except ValueError:
            print("Tricksie hobbits")
            exit(1)
        interface.process(int(userInput))

