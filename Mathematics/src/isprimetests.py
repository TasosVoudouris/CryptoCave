import timeit
from math import sqrt


def is_prime(n):
    '''
    Checks whether the argument n is a prime number.
    Uses a brute force search for factors between 2 and n-1.
    '''
    for j in range(2, n):
        if n % j == 0:
            print(f"{j} is a factor of {n}.")
            return False
    return True


def is_prime_slow(n):
    '''
    Checks whether n is a prime number.
    Searches for factors from 2 up to sqrt(n),
    but recomputes sqrt(n) in each iteration.
    '''
    j = 2
    while j <= sqrt(n):
        if n % j == 0:
            print(f"{j} is a factor of {n}.")
            return False
        j += 1
    return True

def is_prime_fast(n):
    '''
    Checks whether n is a prime number.
    Searches for factors from 2 up to sqrt(n),
    computing sqrt(n) once before the loop.
    '''
    j = 2
    root_n = sqrt(n)
    while j <= root_n:
        if n % j == 0:
            print(f"{j} is a factor of {n}.")
            return False
        j += 1
    return True



# Example number to test for primality
n = 10**5 + 7

# Measure execution times
t1 = timeit.timeit('is_prime(n)', globals=globals(), number=10)
t2 = timeit.timeit('is_prime_slow(n)', globals=globals(), number=10)
t3 = timeit.timeit('is_prime_fast(n)', globals=globals(), number=10)

print(f"is_prime:      {t1:.6f} seconds (avg over 10 runs)")
print(f"is_prime_slow: {t2:.6f} seconds (avg over 10 runs)")
print(f"is_prime_fast: {t3:.6f} seconds (avg over 10 runs)")