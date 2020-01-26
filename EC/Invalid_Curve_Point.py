
from sage.all import *
from Crypto.Util.number import *

def Find_Curve(p,a):
    optimal = [1]
    for i in range(1,200):
        Ex = EllipticCurve(GF(p),[a,i]).cardinality()
        s = ecm.factor(Ex)
        s.append(i)
        s[:] = [x for x in s if x != 2]
        l[i] = s         
        if len(optimal) < len(s):
            optimal = s
    return optimal[-1]

def Alice(P):
    secret = bytes_to_long("Invalid Curve Point Secret Key")
    Q = secret*P 
    return Q

def brute_force(P,Q):
    for i in range(1,1000000):
        if P*i==Q:
            return i
    print "failed"
    return 0

def filter_for_CRT(l):
    fa = []
    sa = []
    secret = bytes_to_long("Invalid Curve Point Secret Key")
    for i in l:      
        if secret%i[1]==i[0]:
            fa.append(i[0])
            sa.append(i[1])
        else:
            print "Damn"
    return CRT(fa,sa)


def Attack(E):
    modl = [2,3,7]
    ans = []
    fa =[]
    sa =[]
    while(1):
        try:   
            Ec = EllipticCurve(GF(p),[a,randint(1,1231231231234124)]) 
            order = Ec.order()
            P = Ec.random_point()
            fac = ecm.factor(order)
            print "Curve Calculated, Order Found, Order Calculated"
            for i in fac:
                if i not in modl and i < 1000000:
                    Pi = (order//i)*P
                    Qi = Alice(Pi)
                    x = brute_force(Pi,Qi)
                    print "Found!!!"
                    ans.append([x,i])
                    modl.append(i)
        except:
            pass
        if (mul(modl)//2) > 506805544377210991192709769824062628134365276883090959977357114717463929:
            break
    return ans
                

        
        

if __name__=="__main__":
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    a = p-3
    E = EllipticCurve(GF(p),[a,b])
    cr = Attack(E)
    flag = filter_for_CRT(cr)
    print long_to_bytes(flag)
