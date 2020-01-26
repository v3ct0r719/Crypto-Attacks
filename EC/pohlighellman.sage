
def pohlighellman(ec,P,Q):
    n = P.order()
    factors = list(factor(n))
    li = []
    modi = []
    for p,e in factors[:-1]:
        P0 = (n//p) * P
        z = []
        for i in range(e):
            multiplier = (n // (p**(i+1)))
            BASE = Q
            for j in range(len(z)):
                BASE -= z[j] * (p**j) * P    
            Q0 = multiplier * BASE
            z.append(P0.discrete_log(Q0))
        l0 = 0
        for i in range(e):
            l0 += z[i] * (p**i)
        li.append(l0)
        modi.append(p**e)

    return crt(li,modi)

def test():
    ## Parameters from "Alice Sends Bob a meme"
    p = 108453893951105886914206677306984937223705600011149354906282902016584483568647
    a = 829
    b = 512

    # Curve is y^2 = X^3 + ax^2 + b
    # this is different from the normal curve
    ec = EllipticCurve(GF(p),[0,a,0,b,0])
    P = (88610873236405736097813831550942828314268128800347374801890968111325912062058, 76792255969188554519144464321650537182337412449605253325780015124365585152539)
    Q = (27543889954945113502256551007964501073506795938025836235838339960818915950890, 75922969573987021583641685217441284832467954055295272505357185824478295962572)
    P = ec(P)
    Q = ec(Q)
    l_bound = 84442469965344
    l = pohlighellman(ec,P,Q)
    print l,l==1213123123131

def test2():
    ## Parameters from "Cryptopals Challenge 59"
    p = 233970423115425145524320034830162017933
    a = -95051
    b_list = [210,504,727]

    ## Curve is y^2 = x^3 + ax + b
    for b in b_list:
        ec = EllipticCurve(GF(p),[a,b])
        
        P = ec.random_point()
        import random
        l = random.randint(1234,1234123412)
        Q = l*P
        res = pohlighellman(ec,P,Q)
        print res,res == l

test2()
