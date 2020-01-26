#!/usr/bin/env python2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os, sys

from secret import AES_KEY, FLAG

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

class CryptoError(Exception):
    pass

def split_by(data, step):
    return [data[i : i+step] for i in xrange(0, len(data), step)]

def xor(a, b):
    assert len(a) == len(b)
    return ''.join([chr(ord(ai)^ord(bi)) for ai, bi in zip(a,b)])

def pad(m):
    padbyte = 16 - (len(m) % 16)
    return m + padbyte*chr(padbyte)

def unpad(m):
    if not m:
        return ''
    lastchar = ord(m[-1])
    return m[:-lastchar]

def _encrypt(aes, msg):
    msg = pad(msg)
    iv = get_random_bytes(16)
    prev_pt = iv
    prev_ct = iv
    ct = ""
    for block in split_by(msg, 16) + [iv]:
        ct_block = xor(block, prev_pt)
        ct_block = aes.encrypt(ct_block)
        ct_block = xor(ct_block, prev_ct)
        ct += ct_block
        prev_pt = block
        prev_ct = ct_block
    return iv + ct

def _decrypt(aes, msg):
    iv, msg = msg[:16], msg[16:]
    prev_pt = iv
    prev_ct = iv
    pt = ''
    for block in split_by(msg, 16):
        pt_block = xor(block, prev_ct)
        pt_block = aes.decrypt(pt_block)
        pt_block = xor(pt_block, prev_pt)
        pt += pt_block
        prev_pt = pt_block
        prev_ct = block
    pt, mac = pt[:-16], pt[-16:]
    if mac != iv:
        print "[-] Authentication Error!"
        raise CryptoError()
    return unpad(pt)

if __name__ == "__main__":
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    try:
        while True:
            print ""
            a = raw_input("Enter the plaintext: ")
            try:
                b = raw_input("Enter the ciphertext(in hex): ").decode("hex")
            except:
                print "[-] Enter proper hex chars!"
                sys.exit(0)
            b = _decrypt(aes, b)
            if a == b:
                if a == "gimme_flag":
                    print _encrypt(aes, FLAG).encode("hex")
                else:
                    print _encrypt(aes, get_random_bytes(len(FLAG))).encode("hex")
            else:
                print "[-] Looks like you don't know the secret key? Too bad."
    except:
        print "[-] Something's Wrong!"
        sys.exit(0)
