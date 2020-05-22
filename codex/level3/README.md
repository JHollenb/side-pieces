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
* Export - Export the contents of the DB to a csv in the current directory.
* Clear all - Clear all entries in the DB.

# Design
From a high-level, the program operates as follows:

1. User spins up the executable 
1. User tells the program what they want to do
1. User provides input to accomplish what they want to do
1. This process is repeated on loop until the user wish to exit

To do this, I created a `DbInterface` class and a `UserInterface` class. The `DbInterface` class is responsible for all things database related; initialization, reads, writes, etc. The `UserInterface` class is responsible for interacting with the users. The includes the display and user input. 

## `DbInterface`
The `DbInterface` is built around sqlite. I didn't want to deal with the configurations involved with other databases, launching another process etc. I wanted something light and fast. The sqlite program creates a file that we are able to read and write to. I thought that this would suffice for this project.

I check the input using Safe Query Parameters. This breaks
## `UserInterface`

# Security
# Testing

