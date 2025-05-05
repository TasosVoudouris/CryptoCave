import random
from math import gcd as GCD
from Crypto.Util.number import getPrime
#from sympy.ntheory import jacobi_symbol

################ CUSTOM JACOBI SYMBOL IMPLEMENTATION #########################

def jacobi_symbol(a, n):
    if a ==0:
        return 0
    if a ==1:
        return 1
    #write a = 2^e *s where a1 is odd
    e =0
    a1 = a
    while a1 & 1==0: #while a1 is even
        a1>>=1
        e+=1
        
    #if e is even set s = 1
    if e & 1 == 0:
        s = 1
    elif n % 8 == 7 or n % 8 == 1:
        s = 1
    elif n % 8 == 3 or n % 8 == 5:
        s = -1
    
    if n % 4 == 3 and a1 % 4 == 3:
        s = -s
        
    n1 = n % a1
    if a1 ==1:
        return s
    else:
        return s * jacobi_symbol(n1, a1)

def solovay_strassen_test(n, k):
    if n < 3 or n % 2 == 0:
        return 'Composite'
    for _ in range(k):
        a = random.randint(2, n - 2)
        if GCD(a, n) != 1:
            return 'Composite'
        r = pow(a, (n - 1) // 2, n)
        jac = jacobi_symbol(a, n) % n  # Jacobi symbol can be -1 or 1, mod n ensures comparison
        if r != jac:
            return 'Composite'
    return 'Probably prime'

p = getPrime(512)

print(solovay_strassen_test(2403, 12))      # Known composite
print(solovay_strassen_test(p, 100))        # Large prime
print(solovay_strassen_test(561, 100))      # Carmichael number — still detected!