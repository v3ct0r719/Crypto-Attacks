from Crypto.Util.number import *
from Crypto.Random.random import randint

import gmpy
import key

flag = key.FLAG.encode('hex')

while len(flag) * 4 < 8192:
  flag += '00'

FLAG = long(flag[:-2], 16)

assert FLAG <= 2**8192

def get_random_prime(bits=1024):
  return int(gmpy.next_prime(randint(2**(bits-1), 2**bits)))

def gen_n(bits=1024):
  p = getStrongPrime(bits/2)
  q = getStrongPrime(bits/2)
  return p*q, p, q

def encrypt(pk, m):
  assert m < pk[0]
  return pow(m, pk[1], pk[0])

def decrypt(pk, sk, c):
  return pow(c, sk[0], pk[0])

def test(n, p, q):
  e = 17 * get_random_prime(20)
  pk, sk = (n, e), (long(gmpy.invert(e, (p-1)*(q-1))), )
  print "[+] RSA Self Test: %r" % (pk, )
  c = encrypt(pk, FLAG)
  print "[+] ciphertext = %d" % c
  m = decrypt(pk, sk, c)
  print "[+] Dec(Enc(m)) == m? : %s" % (m == FLAG)


if __name__ == "__main__":
  n, p, q = gen_n(8192)
  test(n, p, q)
  test(n, p, q)
