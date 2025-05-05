from Crypto.Util.number import isPrime, getPrime, GCD, inverse
import random


def is_prime(n):
    '''
    Checks whether the argument n is a prime number.
    Uses a brute force search for factors between 1 and n.
    '''
    for j in range(2,n):  # the range of numbers 2,3,...,n-1.
        if n%j == 0:  # is n divisible by j?
            print("{} is a factor of {}.".format(j,n))
            return False
    return True


print(is_prime(1345233))

def is_prime(n):
    '''
    Checks whether the argument n is a prime number.
    Uses a brute force search for factors between 1 and n.
    '''
    j = 2
    while j < n:  # j will proceed through the list of numbers 2,3,...,n-1.
        if n%j == 0:  # is n divisible by j?
            print("{} is a factor of {}.".format(j,n))
            return False
        j = j + 1  # There's a Python abbreviation for this:  j += 1.
    return True


def fermat_test(n, k):
    for i in range(k):
        a = random.randint(2, n-2)
        #print(a)
        if GCD(a, n)!=1: ##Remark this should return COMPOSITE (since you found a divisor !=1) but to show the flaw we did it this way
            i-=1
            continue
        if pow(a, n-1, n) != 1:
            return 'Composite'
    return 'Probably prime'

print(fermat_test(2403, 12))
p = getPrime(512)
print(fermat_test(p, 100))

print(f"561 is {fermat_test(561, 100)} but 561 % 3 = {561 % 3}")
print(f"41041 is {fermat_test(41041, 100)} but 41041 % 11 = {41041 % 11}")