from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from pwn import *

def _encrypt(message):
    r.recvuntil("choice: ")
    r.sendline("1")
    r.recvuntil("to encrypt (in hex): ")
    r.sendline(message.encode("hex"))
    ct = r.recvline("ciphertext (in hex): ").strip()[37:]
    r.recvline()
    r.recvline()
    return ct.decode("hex")

def _decrypt(ciphertext):
    r.recvuntil("choice: ")
    r.sendline("2")
    r.recvuntil("to decrypt (in hex): ")
    r.sendline(ciphertext.encode("hex"))
    pt = r.recvline("plaintext (in hex): ").strip()[36:]
    r.recvline()
    r.recvline()
    return pt.decode("hex")

r = process("./run.sh")
#r = remote("18.217.237.201","3197")
r.recvline()
flag_enc = r.recvline().strip()[31:].decode("hex")
N = int(r.recvline().strip()[20:])
r.close()

print "Flag_enc: ", flag_enc.encode("hex")
print "N: ", N

# Public exponent
e = 65537

"""
1. The least significant bit of the flag is 1
2. Can be known by simply sending the ciphertext of the flag to the decryption
oracle
"""
flag = "1"
for i in range(1, 121):
    r = process("./run.sh")
    #r = remote("18.217.237.201","3197")
    r.recvline()
    flag_enc = r.recvline().strip()[31:].decode("hex")
    N = int(r.recvline().strip()[20:])

    # Actual Attack
    inv = inverse(2**i, N)
    chosen_ct = long_to_bytes((bytes_to_long(flag_enc)*pow(inv, e, N)) % N)
    output = _decrypt(chosen_ct)
    assert output == "\x01" or output == "\x00"
    flag_char = (ord(output) - (int(flag, 2)*inv) % N) % 2

    print "Here: ", flag_char
    flag = str(flag_char) + flag
    if len(flag) % 8 == 0:
        print long_to_bytes(int(flag, 2))

    r.close()
