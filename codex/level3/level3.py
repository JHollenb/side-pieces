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

class DB:
    def __init__(self, name='', tableName='users'):
        dbExists = False
        self.cursor = None
        self.tableName = tableName
        self.usefulCmds = {
        'createTable':'''CREATE TABLE {} (name text, 
                                          age integer, 
                                          phone text)'''.format(self.tableName),
                                          
        'doesTableExist':'''SELECT count(name) 
                            FROM sqlite_master 
                            WHERE type='table' AND name='{}' '''.format(self.tableName),

        'addUser':"INSERT INTO {} VALUES ('{}','{}','{}')",
        'selectAll':'SELECT * FROM {} ORDER BY name'.format(self.tableName), 
        'deleteUser':"DELETE FROM {} WHERE name = '{}';",
        'updateUser':"UPDATE {} SET name = '{}', age = {}, phone = '{}' where name = '{}'",
        'clearAllUser':"DELETE FROM {}".format(self.tableName)
        }
        self.open(name)

    def open(self, name):
        dbExists = False
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        if (not self.doesTableExist()):
            self.cmd(self.usefulCmds['createTable'])

    def doesTableExist(self):
        retval = False
        self.cursor.execute(self.usefulCmds['doesTableExist'])
        if (self.cursor.fetchone()[0] == 1): 
            retval = True
        return retval

    def cmd(self, cmd):
        retval = self.cursor.execute(cmd)
        self.conn.commit()
        return retval

    def add(self, name, age, phone):
        self.cmd(self.usefulCmds['addUser'].format(self.tableName, name, age, phone))

    def dump(self):
        for row in self.cmd(self.usefulCmds['selectAll']):
                print(row)

    def remove(self, name):
        try:
            self.cmd(self.usefulCmds['deleteUser'].format(self.tableName, name))
        except sqlite3.OperationalError:
            print("[Error] Could not find user to delete")

    def update(self, oldName, name, age, phone):
        self.cmd(self.usefulCmds['updateUser'].format(self.tableName, name, age, phone, oldName))

    def clearAll(self):
        self.cmd(self.usefulCmds['clearAllUser'])

    def export(self, fileName='tmp.csv'):
        self.cmd(self.usefulCmds['selectAll'])
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

class personDB:
    def __init__(self, name='', age=0, phone=''):
        self.name = name
        self.age = age
        self.phone = phone
        self.db = DB("database.db")

        '''
        if len(name) is 0 or len(age) is 0:
            print("Must enter a name and age")
            exit(1)
        '''

    def add(self):
        print("Called add...")
        name = str(input("Name: "))
        age = input("Age: ")
        phone = input("Phone: ")
        self.db.add(name, age, phone)

    def remove(self):
        print("Called remove...")
        name = str(input("Whom shall we delete? "))
        self.db.remove(name)

    def edit(self):
        print("Called edit...")
        oldName = str(input("old name: "))
        name = str(input("new name: "))
        age = input("new age: ")

        try:
            age = int(age)
        except ValueError:
            print("Tricksie hobbits, age is a number, not a construct")
            exit(1)
        phone = input("new phone: ")

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
    myDB = personDB()

    while(1):
        myDB.printBanner()
        userInput = input('==> ')
        try:
            userInput = int(userInput)
        except ValueError:
            print("Tricksie hobbits")
            exit(1)
        myDB.process(int(userInput))

