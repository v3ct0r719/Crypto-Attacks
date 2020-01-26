
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from gmpy2 import *
from pwn import *


def encrypt(m):
        return pow(m,e,n)
def decrypt(c):
	io.sendline('2')
	io.sendline(long_to_bytes(c).encode('hex'))
	io.recvuntil('Here take your plaintext (in hex):  ') 
	x = io.recv().split('\n')[0]
	if x == '00':
		return 0
	else:
		return 1


if __name__ == '__main__':
	io = process("./bin.sh")
        context.log_level = "debug"
        io.recv()
        x = io.recv().split()
        c = x[0]
        c = int(c,16)
        n = int(x[4])
        e = 65537
        inv = pow(2,e,n)
        low = 0
        high = n
	for _ in range(2048-120):
		high = (low + high)/2
	for i in range(120):
		io = process('./bin.sh')
		context.log_level = "debug"
		io.recv()
		x = io.recv().split()
		c = int(x[0],16)
		n = int(x[4])
		inv = pow(2,e,n)
		for j in range(2048-120):
			c = (c * inv) % n
		for k in range(i+1):
			c = (c * inv) % n		
		if decrypt(c)==0:
			high = (low + high)/2
		else:
			low = (low + high)/2
		if 'w0w' in long_to_bytes(high):
			print (long_to_bytes(high))
			break
			
	print long_to_bytes(high)
