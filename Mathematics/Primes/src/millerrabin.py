import random
from Crypto.Util.number import getPrime

def miller_rabin_test(n, k):
    '''
    Arguments: 
        n: int -- number to be tested
        k: int -- number of trials
    Return: `Composite` or `Probably prime`'''
    
    #check parity
    if not n & 1:
        return 'Composite'
    
    r = 0
    s = n-1
    #write n-1 = 2^r*s
    while not s & 1:
        s = s>>1
        r+=1
    assert(pow(2, r)* s == n-1)
    
    for i in range(k):
        a = random.randint(2, n-2)
        x = pow(a, s, n)
        if x == 1 or x == n-1:
            continue #search for another witness
        for _ in range(r):
            x = pow(x, 2, n)
            if x == n-1:
                break 
        else:
             #if it doesnt break, neither condition is satisfied =>  this executes => we found a composite
            return "Composite"
    return "Probably prime"

print(miller_rabin_test(2403, 100))
p = getPrime(512)
print(miller_rabin_test(p, 100))
print(miller_rabin_test(561, 100))