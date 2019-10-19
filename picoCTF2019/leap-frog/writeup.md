## leap-frog

This a ROP challenge which basically wants us to set three boolean values to true in order to get the flag.

There is an obvious overflow in the vuln function. From here jumping to `leapA` is easy and sets the value of win1 for us.

Now the real challenge was setting win3 to true, which can't be done by jumping to any part in leap2 as it is using pc relative addressing using the `x86.get_pc_thunk.ax`. We need to do this using some sort of *ROP* chain.

I looked at leapA's disassembly:
   0x080485e6 <+0>:		push   ebp
   0x080485e7 <+1>:		mov    ebp,esp
   0x080485e9 <+3>:		call   0x804882d <\_\_x86.get\_pc\_thunk.ax>
   0x080485ee <+8>:		add    eax,0x1a12
   0x080485f3 <+13>:	mov    BYTE PTR [eax+0x3d],0x1
   0x080485fa <+20>:	nop
   0x080485fb <+21>:	pop    ebp
   0x080485fc <+22>:	ret 

Here, the useful thing is from +8 , so if we can get the correct value in eax gand jump to leapA + 8 , we can set the value of win3.

win3 = 0x804a03f
win3 - 0x1a12 - 0x3d = **0x80485f0** (target eax value)

we can use the same `x86.get_pc_thunk.ax` to get some value in our eax register. This however should be the address of some instruction, so that ret can execute. Using ROPgadget shows me a gadget at 0x080485c8:
> 0x080485c8 : add al, 8 ; add ecx, ecx ; ret

Using this to add sufficient times to get desired eax value is possible : 0x080485c8 + 8\*5 =  0x80485f0

After this we jump to leapA + 8 to set win3
Note, that we also need to add a fake saved ebp that would be popped inside that function

After this a simple jump to leap2 with the desired arguements and then a jump to display flag to win :).

