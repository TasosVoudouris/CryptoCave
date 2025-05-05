from mpmath import *
import random
# The mpmath package allows us to compute with arbitrary precision!

def prob_prime(N, witnesses):
    '''
    Conservatively estimates the probability of primality, given a positive test result.
    N is an approximation of the size of the tested number.
    witnesses is the number of witnesses.
    '''
    mp.dps = witnesses # mp.dps is the number of digits of precision.  We adapt this as needed for input.
    prob_prime = 1 - (log(N) - 1) / (4**witnesses)
    print(str(100*prob_prime)+"% chance of primality") # Use str to convert mpmath float to string for printing.
prob_prime(10**100, 50) # Chance of primality with 50 witnesses, if a 100-digit number is tested.

def Miller_Rabin(p, base):
    '''
    Tests whether p is prime, using the given base.
    The result False implies that p is definitely not prime.
    The result True implies that p **might** be prime.
    It is not a perfect test!
    '''
    result = 1
    exponent = p-1
    modulus = p
    bitstring = bin(exponent)[2:] # Chop off the '0b' part of the binary expansion of exponent
    for bit in bitstring: # Iterates through the "letters" of the string.  Here the letters are '0' or '1'.
        sq_result = result*result % modulus  # We need to compute this in any case.
        if sq_result == 1:
            if (result != 1) and (result != exponent):  # Note that exponent is congruent to -1, mod p.
                return False  # a ROO violation occurred, so p is not prime
        if bit == '0':
            result = sq_result 
        if bit == '1':
            result = (sq_result * base) % modulus
    if result != 1:
        return False  # a FLT violation occurred, so p is not prime.
    
    return True  # If we made it this far, no violation occurred and p might be prime.

# We implement the Miller-Rabin test for primality in the `is_prime` function below.
def is_prime(p, witnesses=50):  # witnesses is a parameter with a default value.
    '''
    Tests whether a positive integer p is prime.
    For p < 2^64, the test is deterministic, using known good witnesses.
    Good witnesses come from a table at Wikipedia's article on the Miller-Rabin test,
    based on research by Pomerance, Selfridge and Wagstaff, Jaeschke, Jiang and Deng.
    For larger p, a number (by default, 50) of witnesses are chosen at random.
    '''
    if (p%2 == 0): # Might as well take care of even numbers at the outset!
        if p == 2:
            return True
        else:
            return False 
    
    if p > 2**64:  # We use the probabilistic test for large p.
        trial = 0
        while trial < witnesses:
            trial = trial + 1
            witness = random.randint(2,p-2) # A good range for possible witnesses
            if Miller_Rabin(p,witness) == False:
                return False
        return True
    
    else:  # We use a determinisic test for p <= 2**64.
        verdict = Miller_Rabin(p,2)
        if p < 2047:
            return verdict # The witness 2 suffices.
        verdict = verdict and Miller_Rabin(p,3)
        if p < 1373653:
            return verdict # The witnesses 2 and 3 suffice.
        verdict = verdict and Miller_Rabin(p,5)
        if p < 25326001:
            return verdict # The witnesses 2,3,5 suffice.
        verdict = verdict and Miller_Rabin(p,7)
        if p < 3215031751:
            return verdict # The witnesses 2,3,5,7 suffice.
        verdict = verdict and Miller_Rabin(p,11)
        if p < 2152302898747:
            return verdict # The witnesses 2,3,5,7,11 suffice.
        verdict = verdict and Miller_Rabin(p,13)
        if p < 3474749660383:
            return verdict # The witnesses 2,3,5,7,11,13 suffice.
        verdict = verdict and Miller_Rabin(p,17)
        if p < 341550071728321:
            return verdict # The witnesses 2,3,5,7,11,17 suffice.
        verdict = verdict and Miller_Rabin(p,19) and Miller_Rabin(p,23)
        if p < 3825123056546413051:
            return verdict # The witnesses 2,3,5,7,11,17,19,23 suffice.
        verdict = verdict and Miller_Rabin(p,29) and Miller_Rabin(p,31) and Miller_Rabin(p,37)
        return verdict # The witnesses 2,3,5,7,11,17,19,23,29,31,37 suffice for testing up to 2^64. 
    
print(is_prime(1000000000000066600000000000001))  # This is Belphegor's prime.
for p in range(1,1000):
    if is_prime(p):  # We only need to check these p.
        M = 2**p - 1 # A candidate for a Mersenne prime.
        if is_prime(M):
            print("2^{} - 1 = {} is a Mersenne prime.".format(p,M))