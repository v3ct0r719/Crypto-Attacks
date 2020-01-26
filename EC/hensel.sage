from sage.all import *

def hensel_lift(E, p, P):
    A, B = long(E.a4()), long(E.a6())
    x, y = map(long,P.xy())

    pol = y**2 - (x**3 + A*x + B)
    t = (- pol / p) % p 
    t *= inverse_mod(2 * y, p) 
    t = t%p 
    new_y = y + p * t
    return x, new_y

if __name__=="__main__":
	p = 78073891682999454118737679765438614084993542044291616564016048660626381711753L
	A = 519977917294380552733586152195L
	B = 318299294286222680443210554841L
	E = EllipticCurve(GF(p),[A,B])
	P = E.gens()[0]
	print hensel_lift(E, p ,P)

















