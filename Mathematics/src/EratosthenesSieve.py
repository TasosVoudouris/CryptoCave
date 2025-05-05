from math import sqrt
import timeit

def isprime_list(n):
    ''' 
    Return a list of length n+1
    with Trues at prime indices and Falses at composite indices.
    '''
    flags = [True] * (n+1)  # A list [True, True, True,...] to start.
    flags[0] = False  # Zero is not prime.  So its flag is set to False.
    flags[1] = False  # One is not prime.  So its flag is set to False.
    p = 2  # The first prime is 2.  And we start sieving by multiples of 2.
    
    while p <= sqrt(n):  # We only need to sieve by p is p <= sqrt(n).
        if flags[p]:  # We sieve the multiples of p if flags[p]=True.
            flags[p*p::p] = [False] * len(flags[p*p::p]) # Sieves out multiples of p, starting at p*p.
        p = p + 1 # Try the next value of p.
        
    return flags

def where(L):
    '''
    Take a list of booleans as input and
    outputs the list of indices where True occurs.
    '''
    return [n for n in range(len(L)) if L[n]]

#print(where(isprime_list(100)))

#print(sum(isprime_list(1000000)))  # The number of primes up to a million!

t1 = timeit.timeit('sum(isprime_list(1000000))', globals=globals(), number=1)
print(t1)


def isprime_list_fast(n):
    ''' 
    Return a list of length n+1
    with Trues at prime indices and Falses at composite indices.
    '''
    flags = [True] * (n+1)  # A list [True, True, True,...] to start.
    flags[0] = False  # Zero is not prime.  So its flag is set to False.
    flags[1] = False  # One is not prime.  So its flag is set to False.
    flags[4::2] = [False] * ((n-2)//2)
    p = 3
    while p <= sqrt(n):  # We only need to sieve by p is p <= sqrt(n).
        if flags[p]:  # We sieve the multiples of p if flags[p]=True.
            flags[p*p::2*p] = [False] * len(flags[p*p::2*p]) # Sieves out multiples of p, starting at p*p.
        p = p + 2 # Try the next value of p.  Note that we can proceed only through odd p!
        
    return flags

t2 = timeit.timeit('sum(isprime_list_fast(1000000))', globals=globals(), number=1)
print(t2)

def isprime_list_fastest(n):
    ''' 
    Return a list of length n+1
    with Trues at prime indices and Falses at composite indices.
    '''
    flags = [True] * (n+1)  # A list [True, True, True,...] to start.
    flags[0] = False  # Zero is not prime.  So its flag is set to False.
    flags[1] = False  # One is not prime.  So its flag is set to False.
    flags[4::2] = [False] * ((n-2)//2)
    p = 3
    while p <= sqrt(n):  # We only need to sieve by p is p <= sqrt(n).
        if flags[p]:  # We sieve the multiples of p if flags[p]=True.
            flags[p*p::2*p] = [False] * ((n-p*p-1)//(2*p)+1) # Sieves out multiples of p, starting at p*p.
        p = p + 2 # Try the next value of p.
        
    return flags


t3 = timeit.timeit('sum(isprime_list_fastest(1000000))', globals=globals(), number=1)
print(t3)