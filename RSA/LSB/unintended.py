from pwn import *
import time

if __name__=="__main__":
    n_list = []
    c_list = []
    for i in range(65537):
        try:
            io = process('./bin.sh')
            io.recv()
            x = io.recv().split()
            c = x[0]
            print i
            c = int(c,16)
            n = int(x[4])
            n_list.append(n)
            c_list.append(c)
            io.close()
        except:
            time.sleep(2)
            pass










