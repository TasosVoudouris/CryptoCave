from Crypto.Util.number import getPrime
import random
from math import gcd as GCD


def fermat_test(n, k):
    for _ in range(k):
        a = random.randint(2, n - 2)
        if GCD(a, n) != 1:
            continue  # You may optionally return 'Composite' here instead
        if pow(a, n - 1, n) != 1:
            return 'Composite'
    return 'Probably prime'    
print(fermat_test(2403, 12))  # Composite number

p = getPrime(512)
print(fermat_test(p, 100))   # Large probable prime  

print(f"561 is {fermat_test(561, 100)} but 561 % 3 = {561 % 3}")     # 561 is Carmichael
print(f"41041 is {fermat_test(41041, 100)} but 41041 % 11 = {41041 % 11}")  # 41041 is also Carmichael