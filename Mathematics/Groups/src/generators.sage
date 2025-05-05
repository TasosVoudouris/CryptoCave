def checkgen(g, p):
    if is_prime(p) == False: 
        return "not a prime"
    if gcd(g, p) != 1:
        return "not invertible mod p"
    result = True;
    n = p - 1  # order of GF(p)
    for q in prime_factors(n):
        b = power_mod(g, n // q, p)
        if b == 1:
            result = False  # g is not a generator
            break
    return result

p = 2535301200456458802993406412663
g = 3
print(checkgen(g, p))
g = 5
print(checkgen(g, p))

#######################################################################################

p = 17  # 3 5 6 7 10 11 12 14
print("p =", p)
print("p is a prime number:", p in Primes())

F = GF(p)
print("Powers of the first column modulo", p)
for g in range(1, p): 
    for k in range(1, p):
        if F(g) ^ k <= 9:
            print(F(g) ^ k, end="  ")
        else:
            print(F(g) ^ k, end=" ")
    print()

g = F(primitive_root(p))
print("Number of generators =", euler_phi(p - 1))
print("A generator =", g)
for k in range(1, p):
    print(g, "^", k, "=", F(g) ^ k)

print("What are the other generators?")
phi = euler_phi(p - 1)

generators = [power_mod(g, k, p) for k in range(1, p) if gcd(k, p - 1) == 1]
generators.sort()
print("All generators of Z*_%d:" % p, generators)

