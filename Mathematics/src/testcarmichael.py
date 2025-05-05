from sympy import isprime, gcd
from sympy.ntheory.factor_ import factorint

def is_carmichael(n):
    # Carmichael numbers must be square-free and composite
    if isprime(n):
        return False

    factors = factorint(n)
    # Must be square-free (no repeated prime factors)
    if any(exp > 1 for exp in factors.values()):
        return False

    # For all prime divisors p of n, p - 1 must divide n - 1
    for p in factors.keys():
        if (n - 1) % (p - 1) != 0:
            return False

    return True

# Test the given number
# n = 862978178865374730139845690278208781767603294507602119220311853
print(is_carmichael(n))