from sympy import nextprime, legendre_symbol, isprime, mod_inverse
from sympy.ntheory.modular import crt
from random import randint, choice
from math import prod as product

def generate_S_a(a_list, p_bound):
    """Generate S[a] = { p mod 4a : p prime < p_bound, (a|p) = -1 }."""
    S = {a: set() for a in a_list}
    for a in a_list:
        p = 3
        while p < p_bound:
            if legendre_symbol(a, p) == -1:
                S[a].add(p % (4 * a))
            p = nextprime(p)
    return S

def random_prime_below(bound, lbound=2):
    """Return a random prime in [lbound, bound]."""
    while True:
        p = randint(lbound, bound)
        if isprime(p):
            return p

def get_k(h, a_list, prime_bound):
    """Generate k_list = [1, k2, …, kh] of distinct primes ≠ any a in a_list."""
    k_list = [1]
    for _ in range(1, h):
        while True:
            k = random_prime_below(prime_bound)
            if k not in a_list and k not in k_list:
                k_list.append(k)
                break
    return k_list

def find_subsets_S(S, a_list, k_list):
    """For each a, intersect the sets {(inv_k*(s + k – 1)) mod 4a : s ∈ S[a]} over k in k_list."""
    S_sub = {}
    for a in a_list:
        temp = []
        for k in k_list:
            invk = mod_inverse(k, 4*a)
            transformed = {(invk * (s + k - 1)) % (4*a) for s in S[a]}
            temp.append(transformed)
        S_sub[a] = set.intersection(*temp)
    return S_sub

def choose_z(S_sub, a_list):
    """Pick a random residue z_a ∈ S_sub[a] for each a."""
    return {a: choice(tuple(S_sub[a])) for a in a_list}

def create_and_solve_conditions(a_list, zs, k_list):
    """
    Build and solve CRT:
      x ≡ zs[a]      (mod 4a)  for each a
      x ≡ -1/k2      (mod k3)
      x ≡ -1/k3      (mod k2)
    Returns (x, m) where m = ∏ moduli.
    """
    residues = [zs[a] for a in a_list] + [
        mod_inverse(-k_list[1], k_list[2]),
        mod_inverse(-k_list[2], k_list[1])
    ]
    moduli   = [4*a for a in a_list] + [k_list[2], k_list[1]]

    result = crt(moduli, residues)
    if result is None:
        raise ValueError("CRT failed: no solution for these congruences")
    x, _ = result
    m = product(moduli)
    return x, m

def get_pseudoprime(x, m, k_list,
                    starting_bitsize=128,
                    max_attempts=1_000_000):
    """
    Search for p1 = i*m + x of bit-length ≥ starting_bitsize
    such that p1 and each k*(p1–1)+1 are prime.
    """
    bit_m = m.bit_length()
    i = 2**(starting_bitsize - bit_m) if starting_bitsize > bit_m else 1
    p1 = i*m + x

    for attempt in range(max_attempts):
        if attempt % 50_000 == 0:
            print(f"Attempt {attempt}: p1 bit-length = {p1.bit_length()}")
        if isprime(p1):
            chain = [p1]
            for k in k_list[1:]:
                c = k*(p1 - 1) + 1
                if not isprime(c):
                    break
                chain.append(c)
            else:
                return product(chain), chain
        p1 += m

    raise RuntimeError("Exceeded max_attempts without finding a full pseudoprime chain")


if __name__ == "__main__":
    # Parameters (tweak these for speed vs. difficulty)
    a_list    = [2, 3, 5, 7]
    p_bound   = 1000
    k_bound   = 300
    h         = 3
    bit_target= 64        # start small for testing
    max_tries = 2_000_000

    # 1) build S
    S = generate_S_a(a_list, p_bound)

    # 2) find compatible k_list, S_sub, CRT solution
    while True:
        k_list = get_k(h, a_list, k_bound)
        S_sub   = find_subsets_S(S, a_list, k_list)
        if any(len(s) == 0 for s in S_sub.values()):
            continue
        try:
            zs = choose_z(S_sub, a_list)
            x, m = create_and_solve_conditions(a_list, zs, k_list)
            break
        except ValueError:
            continue

    print("Found CRT solution; now searching for pseudoprime chain…")

    # 3) search for the chain
    p, chain = get_pseudoprime(
        x, m, k_list,
        starting_bitsize=bit_target,
        max_attempts=max_tries
    )

    print("Chain‐product pseudoprime:", p)
    print("Prime chain factors:", chain)
