
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
	return x
def oracle(c):
	x = decrypt(c)
	if x == '00':
		return 0
	else:
		return 1
	

if __name__ == '__main__':
	#io = remote("13.233.196.46", 8671)
        io = process('./bin.sh')
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
	for i in range(2048-120):
		c = (inv * c)%n
		high = (low+high)/2
	for j in range(120):
		c = (inv * c)%n
		if oracle(c) == 0:
			high = (low + high)/2
		else:
			low = (low + high)/2
	print long_to_bytes(high)	
    
