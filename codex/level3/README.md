# Level 3
Create a command-line based user interface program that:
1. Accepts 3 command line parameters
    - Required: name and age
    - Optional: phone number
1. Stores the data in a database
1. Supports the following commands:
    - User:
        1. Add
        2. Remove
        3. Edit
    - Database:
        1. Export
        2. Clear
    - Print all users (in table format, sorted by name, with all attributes) to stdout or a file

# Overview
Although the instructions prescribed that the program accept three command line parameters, I opted for a different approach (note that I left code in to go back to the >three parameter design).

In my approach, the user start the program via command line in linux `./level3`.

From here the user is given a display with several options. The display looks like this:
```
$ ./level3.py
================================================================================
Select one of the following options:
--------------------------------------------------------------------------------
0. Quit
1. Add
2. Remove
3. Edit
4. Dump
5. Export
6. Clear all
================================================================================
==>
```

The options are as follows:

* Quit - Exit the program (the user can also enter any key no listed)
* Add - Add a user. From here, the user will input three parameters, `name`, `age`, and `phone`
* Remove - Remove a user. The user provides the name and that row is removed.
* Edit - Edit a users information. 
* Dump - Dump the contents of the user table to the CLI.
* Export - Export the contents of the DB to a csv in the current directory. The default name for this file is `dbDump.csv`.
* Clear all - Clear all entries in the DB.

# Design
From a high-level, the program operates as follows:

1. User spins up the executable 
1. User tells the program what they want to do
1. User provides input to accomplish what they want to do
1. This process is repeated on loop until the user wish to exit

To do this, I created a `DbInterface` class and a `UserInterface` class. The `DbInterface` class is responsible for all things database related; initialization, reads, writes, etc. The `UserInterface` class is responsible for interacting with the users. The includes the display and user input. 

## `DbInterface`
The `DbInterface` is built around sqlite. I didn't want to deal with the configurations 
involved with other databases, launching another process etc. I wanted something light and 
fast. The sqlite program creates a file that we are able to read and write to. I thought 
that this would suffice for this project.

I realized that this application maybe vulnerable to sql injection attacks and sure enough, it
was. A solution I found in sqlite's documentation:

>Instead, use the DB-API’s parameter substitution. Put ? as a placeholder wherever you want to 
>use a value, and then provide a tuple of values as the second argument to the cursor’s 
>execute() method. For example:
>` c.execute('SELECT * FROM stocks WHERE symbol=?', t)`

Per [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), parameterized queries should be the first defense against sql injections.


## `UserInterface`
The `UserInterface` spins on a forever loop, waiting for user input. The user input is verified 
via the `check_input()` function. This does not santize input but can be used for that. This 
function currently only tries to cast values to either an `int` or a `string`.

Depending on what the user input, a call is made to the `DbInterface`. The `UserInterface` 
contains a handle to the `DbInterace`. The `DbInterface` will handle all DB interactions. 
