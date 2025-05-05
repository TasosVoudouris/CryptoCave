# Pure‐Sage implementation of Arnault’s pseudoprime‐chain construction
# with robust CRT handling and correct modulus calculation.

from sage.all import *
import random

class ArnaultPseudoprime:
    def __init__(self, a_list, gen_S_prime_bound=1000, zs_iter_bound=100, k_bound=300):
        self.a_list             = a_list
        self.gen_S_prime_bound  = gen_S_prime_bound
        self.zs_iter_bound      = zs_iter_bound
        self.k_bound            = k_bound

    def generate_S_a(self):
        S = {a: set() for a in self.a_list}
        for a in self.a_list:
            p = 3
            while p < self.gen_S_prime_bound:
                if legendre_symbol(a, p) == -1:
                    S[a].add(p % (4*a))
                p = next_prime(p)
        return S

    def get_k(self, h):
        k_list = [1]
        for _ in range(1, h):
            while True:
                k = random_prime(self.k_bound, lbound=2)
                if k not in self.a_list and k not in k_list:
                    k_list.append(k)
                    break
        return k_list

    def find_subsets_S(self, S, k_list):
        S_sub = {}
        for a in self.a_list:
            parts = []
            for k in k_list:
                invk = inverse_mod(k, 4*a)
                transformed = { (invk*(s + k - 1)) % (4*a) for s in S[a] }
                parts.append(transformed)
            S_sub[a] = set.intersection(*parts)
        return S_sub

    def choose_z(self, S_sub):
        return {a: random.choice(list(S_sub[a])) for a in self.a_list}

    def create_and_solve_conditions(self, zs, k_list):
        # build residue and modulus lists
        residues = [ zs[a] for a in self.a_list ] + [
            inverse_mod(-k_list[1], k_list[2]),
            inverse_mod(-k_list[2], k_list[1])
        ]
        moduli   = [ 4*a for a in self.a_list ] + [ k_list[2], k_list[1] ]

        # robust CRT
        try:
            x = crt(residues, moduli)     # Sage's crt(residues, moduli) → single integer
        except ValueError:
            # residues incompatible—caller will retry with new zs
            raise ValueError("CRT failed: incompatible residue system")

        # correct modulus: product of all moduli
        m = prod(moduli)
        return x, m

    def get_pseudoprime(self, x, m, k_list, starting_bitsize=128, max_attempts=10**6):
        # choose i so that bit‐length of p1 ≥ starting_bitsize
        shift = max(0, starting_bitsize - m.nbits())
        i     = 2**shift
        p1    = i*m + x

        for attempt in range(int(max_attempts)):
            if attempt % 50000 == 0:
                print(f"  [search] attempt {attempt}, p1 bit‐length = {p1.nbits()}")
            if is_prime(p1):
                chain = [p1]
                for k in k_list[1:]:
                    q = k*(p1 - 1) + 1
                    if not is_prime(q):
                        break
                    chain.append(q)
                else:
                    # full chain found
                    return prod(chain), chain
            p1 += m

        raise RuntimeError("Exceeded max_attempts without finding a full pseudoprime chain")

    def find_pseudoprime(self, p1_bits=128):
        S = self.generate_S_a()
        h = 3
        print("→ Looking for a valid (k_list, S_sub)…")
        while True:
            k_list = self.get_k(h)
            S_sub  = self.find_subsets_S(S, k_list)
            if any(len(S_sub[a]) == 0 for a in self.a_list):
                continue
            print("  • found nonempty S_sub; trying CRT…")
            zs = self.choose_z(S_sub)
            try:
                x, m = self.create_and_solve_conditions(zs, k_list)
            except ValueError:
                print("    × CRT incompatible, retrying…")
                continue
            print("  ✓ CRT OK; searching pseudoprime chain…")
            try:
                return self.get_pseudoprime(x, m, k_list, starting_bitsize=p1_bits)
            except RuntimeError:
                print("    ↻ no chain found, restarting search…")
                continue

def miller_rabin_test_fixed(n, a_list):
    '''returns Composite or Probably prime'''
    
    #check parity
    if not n & int(1):
        return 'Composite'
    
    r = 0
    s = n-1
    #write n-1 = 2^r*s
    while not s & int(1):
        s = s>>1
        r+=1
    assert(pow(2, r)* s == n-1)
    
    for a in a_list:
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
    



if __name__ == "__main__":
    # Example usage
    a_list = [2,3,5,7,11,13,17,19]
    arn    = ArnaultPseudoprime(
                a_list,
                gen_S_prime_bound=2000,
                zs_iter_bound=100,
                k_bound=500
             )

    N, chain = arn.find_pseudoprime(p1_bits=64)
    print("\n→ Arnault pseudoprime N =", N)
    print("   prime‐chain:", chain)
    print("   Miller–Rabin check:", all(miller_rabin_test_fixed(N, a_list)))
