# Level 1

1. Create a program that reads an ELF file, finds all the strings in it, and writes 
them neatly to a log file.

# Overview
I know that `strings` is already capable of this. In fact, I do this quite often `strings someFile > tmp.log`

So to make a script that does this, I created a python script that uses the `pwntools` library.
This script simply passes an arg to `strings` and then writes the output to `./stringsLog.log`

This application can be called as follows:
```
$ ./level1.py -f <my file>
```
