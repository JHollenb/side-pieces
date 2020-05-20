#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import sys, getopt

def strings(filePath):
    fileStrings = ''
    p = process('strings ' + filePath, shell=True)
    fileStrings = p.recvallS()
    f = open('./stringsLog.log', 'w')
    f.write('-'*80+'\n')
    f.write('Level1: Printing strings from {}\n'.format(filePath))
    f.write('-'*80+'\n')
    f.write(fileStrings)
    f.write('-'*80+'\n')
    f.close()

def printErrBanner():
    print('level1.py -f <file>')
    sys.exit(2)
    
def main(argv):
    filePath = ''
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        printErrBanner()

    if len(opts) == 0:
        printErrBanner()

    for opt, arg in opts:
        if opt == '-h':
            printErrBanner()
        elif opt in ("-f", "--file"):
            filePath = arg
    return filePath

if __name__ == "__main__":
    filePath = main(sys.argv[1:])
    strings(filePath)
