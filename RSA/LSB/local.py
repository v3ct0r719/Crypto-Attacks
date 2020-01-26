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

if __name__ == '__main__':
    #   io = remote("13.233.196.46", 8671)
    e = 65537
    context.log_level = "debug"
    z=0
    flag=''
    for i in range(120):
        io = process('./bin.sh')
        io.recv()
        x = io.recv().split()
        c = x[0]
        c = int(c,16)
        n = int(x[4])
        inv=encrypt(inverse(2**i,n))
	y=(c*inv)%n
	x=int(decrypt(y)[-1:])
	x=(x-inverse(2**i,n)*z%n)%2
	z+=x * 2**i
	flag+=str(x)
        io.close()
    print long_to_bytes(int(flag[::-1],2))	

#    for i in range(120):
#        inv=encrypt(inverse(2**i,n))
#        y = (c * inv)%n
#        ans = decrypt(y)
#        if ans == '00':
#            flag +='0'
#        else:
#            flag += '1'
		
