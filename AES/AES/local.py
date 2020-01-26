from pwn import *
import string
def xor(a,b):
    return "".join(chr(ord(x)^ord(y)) for x,y in zip(a,b))
def send(a,b):
    io.sendline(a)
    io.recv()
    io.sendline(b.encode('hex'))
    x = io.recv()
    return x
def split_by(data, step):
    return [data[i : i+step] for i in xrange(0, len(data), step)]


if __name__ == '__main__':
    
    #io = process('./encrypt.py')
    #context.log_level="debug"
    io = remote('13.233.196.46' ,1337,)
    io.recv()
    wanted = 'gimme_flag'
    main_iv=''
    thing=[]
    hex_char = 'abcdef1234567890'
    for i in range(10):
        iv = main_iv + (chr(16-i-1)*(16-len(main_iv))) 
        print "[+] i:" + str(i) 
        for j in range(256):
            print j
            for k in range(256):
                iv = list(iv)
                iv[i]=chr(j)
                iv[-1:]=chr(k)
                iv = "".join(iv)
                pay = xor(iv,'\x00'*16)
                payload = iv + pay + iv
                x = send(wanted[:i+1],payload)
                if 'like' not in x:
                    if 'cipher' not in x:
                        y= x.split('\n')
                        x=y[0]
                        main_iv+=chr(j)
                        thing.append(x)
                        print x
                        break
                    

    st = string.letters + '0{}_'
    th = thing[-1].split('\n')
    #flag_enc = '34c8c280f3aa2a3f167fe2de824667de69901cd06c1b45db085cb79422ab0aa734c8c280f3aa2a3f167fe2de824667de'.decode('hex')
    flag_enc = th[0].decode('hex')
    flist = split_by(flag_enc,16)
    pay = xor(flist[0],flist[1])

    for i in range(256):
        iv = flist[0][:15]+chr(i)
        load = xor(pay,iv)
        payload = iv+load+iv
        x = send('f',payload)
        if 'like' not in x:
            if 'cipher' not in x:
                y = x.split('\n')
                if len(y[0])==96:
                    lucky_byte = chr(i)
    byte = xor(lucky_byte,chr(15))
    #byte = '\xdc'
    flag = ''        
    for i in range(15,0,-1):
        for j in st:
            iv = flist[0][:15]+xor(byte,chr(i))
            load = xor(pay,iv)
            payload = iv+load+iv
            x = send(flag + j,payload)
            if 'like' not in x:
                if 'cipher' not in x:
                    y = x.split('\n')
                    if len(y[0])==96:
                        flag+=j


        
        

    
