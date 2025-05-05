## Breaking the Miller–Rabin Test: The Arnault Method

- [Breaking the Miller–Rabin Test: The Arnault Method](#breaking-the-millerrabin-test-the-arnault-method)
  - [Constructing Miller–Rabin-Resistant Numbers](#constructing-millerrabin-resistant-numbers)
  - [Quadratic Nonresidue](#quadratic-nonresidue)
  - [Carmichael Numbers Fooling Miller–Rabin](#carmichael-numbers-fooling-millerrabin)
  - [Step 1: Compute Nonresidue Sets $S\_a$](#step-1-compute-nonresidue-sets-s_a)
  - [Step 2: Select Coefficients $k\_i$](#step-2-select-coefficients-k_i)
  - [Step 3: Filter Subsets of Valid Residues $z\_a$](#step-3-filter-subsets-of-valid-residues-z_a)
  - [Step 4: Choose Residue Constraints $z\_a$](#step-4-choose-residue-constraints-z_a)
  - [Step 5: Solve Congruence System via CRT](#step-5-solve-congruence-system-via-crt)
  - [Step 6: Search for Valid $p\_1$, Then Construct Pseudoprime](#step-6-search-for-valid-p_1-then-construct-pseudoprime)
  - [Final Step: Test with Miller–Rabin](#final-step-test-with-millerrabin)
- [Fixed-Base Pseudoprimes: Bleichenbacher’s Construction](#fixed-base-pseudoprimes-bleichenbachers-construction)
  - [Korselt’s Criterion (for Carmichael Numbers)](#korselts-criterion-for-carmichael-numbers)
  - [Erdős's Insight and Bleichenbacher’s Strategy](#erdőss-insight-and-bleichenbachers-strategy)
  - [Pseudoprimes for Fixed Bases](#pseudoprimes-for-fixed-bases)
  - [`generate_M(a_list, prime_idx_bound, random_bound)`](#generate_ma_list-prime_idx_bound-random_bound)
  - [`find_set_R(a_list, M, r_low, r_high)`](#find_set_ra_list-m-r_low-r_high)
  - [`find_subsets_T(R, M)`](#find_subsets_tr-m)
  - [Wrap-Up: What We’ve Learned](#wrap-up-what-weve-learned)



Welcome to the final part of our series on primality testing. In *Part II*, we explored the Fermat test, the Solovay–Strassen test, and the Miller–Rabin test. While the Miller–Rabin test is highly reliable in practice, it is *not infallible*.

In 2018, Henri Arnault demonstrated how to construct *composite numbers that pass the Miller–Rabin test* for many — or even all — fixed bases. These cleverly crafted numbers exploit the structure of *Carmichael numbers* and the properties of *quadratic residues*.

> 📄 *Reference*: [Arnault, ePrint 2018/749](https://eprint.iacr.org/2018/749.pdf)

Arnault’s method is not just a theoretical curiosity — it reveals the *limits of fixed-base probabilistic testing*, even for cryptographic bit-lengths.



We define a version of Miller–Rabin where we test with a *fixed list of bases*, instead of random ones into `millerrabinfixed.py`.

### Constructing Miller–Rabin-Resistant Numbers

Let $n = p_1 p_2 \cdots p_h$ be a Carmichael number, i.e., a composite $n$ such that:

$$
a^{n - 1} \equiv 1 \pmod{n} \quad \forall \, a \text{ with } \gcd(a, n) = 1
$$

We define:

* $k_i = \frac{p_i - 1}{p_1 - 1}$
* $m_i = \frac{\prod_{j \ne i} (p_j - 1)}{p_1 - 1}$

If $k_i, m_i \in \mathbb{Z}$ for all $i$, then $n$ is a Carmichael number.


### Quadratic Nonresidue 

Using *quadratic reciprocity*, we can control the behavior of witnesses:

* If $\gcd(a, n) = 1$ and $\left(\frac{a}{p_i}\right) = -1$ for all $i$, then $a$ becomes a *Miller–Rabin non-witness* for $n$.
* We define a set $S_a \subseteq \mathbb{Z}_{4a}$ of quadratic nonresidues:

  $$
  S_a := \{ p \bmod 4a : \left( \frac{a}{p} \right) = -1 \}
  $$

From this, we infer:

$$
p_1 \bmod 4a \in \bigcap_{i=1}^h k_i^{-1}(S_a + k_i - 1)
$$

This gives congruence constraints on $p_1$, which can be solved via the (CRT).

Below is the pseudocode of the algorithm:

1. *Fix bases* $a_1, a_2, \ldots, a_h$.
2. For each base $a$, compute the quadratic nonresidue set $S_a \subset \mathbb{Z}_{4a}$.
3. Choose $k_i \in \mathbb{Z}$, all coprime to $a$, typically small primes.
4. Construct the intersection:

   $$
   p_1 \bmod 4a \in \bigcap_{i=1}^h k_i^{-1}(S_a + k_i - 1)
   $$
5. For each base $a$, select one valid residue $z_a \in S_a$ → get a system of congruences.
6. Solve using CRT:

   $$
   p_1 \equiv z \pmod{\mathrm{lcm}(4, a_1, \ldots, a_h, k_2, \ldots, k_h)}
   $$
7. Construct:

   $$
   p_i = k_i(p_1 - 1) + 1
   $$

   and test if each $p_i$ is prime.

Result: a composite number $n = p_1 p_2 \cdots p_h$ that passes Miller–Rabin for all chosen bases.


### Carmichael Numbers Fooling Miller–Rabin

Following the *Prime and Prejudice* framework and Arnault 2018), we show a step-by-step construction of a *Miller–Rabin-resistant pseudoprime* using controlled quadratic residue constraints and the CRT:

### Step 1: Compute Nonresidue Sets $S_a$

We compute for each base $a \in A$ the set of residue classes mod $4a$ such that $\left( \frac{a}{p} \right) = -1$:

```python
from sympy import nextprime, legendre_symbol

def generate_S_a(a_list, p_bound):
    S = {a: set() for a in a_list}
    for a in a_list:
        p = 3
        while p < p_bound:
            if legendre_symbol(a, p) == -1:
                S[a].add(p % (4 * a))
            p = nextprime(p)
    return S
```

Usage:

```python
a_list = [2, 3, 5, 7]
S = generate_S_a(a_list, 10000)
```

### Step 2: Select Coefficients $k_i$

Choose distinct primes $k_i$ (coprime to all $a$):

```python
from Crypto.Util.number import getPrime
from random import randint

def random_prime_below(bound, lbound=2):
    from sympy import isprime
    while True:
        p = randint(lbound, bound)
        if isprime(p):
            return p

def get_k(h, a_list, prime_bound):
    k_list = [1]
    for _ in range(1, h):
        while True:
            k = random_prime_below(prime_bound)
            if k not in k_list and k not in a_list:
                k_list.append(k)
                break
    return k_list
```

### Step 3: Filter Subsets of Valid Residues $z_a$

We compute intersections of transformed residue sets using modular inverses:

```python
from sympy import mod_inverse

def inverse_mod(a, m):
    return mod_inverse(a, m)

def find_subsets_S(S, a_list, k_list):
    S_sub = {a: set() for a in a_list}
    for a in a_list:
        temp_sets = []
        for k in k_list:
            temp_set = set()
            inv_k = inverse_mod(k, 4 * a)
            for elem in S[a]:
                new_el = (inv_k * (elem + k - 1)) % (4 * a)
                temp_set.add(new_el)
            temp_sets.append(temp_set)
        S_sub[a] = set.intersection(*temp_sets)
    return S_sub
```

Loop until all intersections are non-empty:

```python
h = 3
while True:
    k_list = get_k(h, a_list, 83)
    S_sub = find_subsets_S(S, a_list, k_list)
    if all(len(s) > 0 for s in S_sub.values()):
        break
```

### Step 4: Choose Residue Constraints $z_a$

Randomly select one residue per base:

```python
from random import choice

def choose_z(S_sub, a_list):
    return {a: choice(tuple(S_sub[a])) for a in a_list}
```

### Step 5: Solve Congruence System via CRT

We collect all modular conditions (including consistency conditions for $p_1$):

```python
from sympy import crt
from math import prod as product

def create_and_solve_conditions(a_list, zs, k_list):
    crt_a_list = [zs[a] for a in a_list] + [
        inverse_mod(-k_list[1], k_list[2]),
        inverse_mod(-k_list[2], k_list[1])
    ]
    crt_m_list = [4 * a for a in a_list] + [k_list[2], k_list[1]]
    x, m = crt(crt_m_list, crt_a_list)
    return int(x), int(m)
```

### Step 6: Search for Valid $p_1$, Then Construct Pseudoprime

```python
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
```

### Final Step: Test with Miller–Rabin

```python
p, p_list = get_pseudoprime(x, m, k_list, starting_bitsize=167)
print("Pseudoprime:", p)
print("Prime factors:", p_list)
print("Miller–Rabin result:", miller_rabin_test_fixed(p, a_list))
```


We provide two implementations of Arnault’s method: one in SageMath (`arnault.sage`) and one in Python (`arnault.py`). They are nearly identical, differing only in the libraries used and the syntax for certain function calls. Both systematically construct an *Arnault pseudoprime*—a composite number $N$ whose prime factors form a recursive “chain” $p_1, p_2, \dots, p_h$, where each

$$
p_{i+1} = k_{i+1} \cdot (p_i - 1) + 1
$$

for small primes $k_2, k_3, \dots$.

The method begins by filtering primes using the Legendre symbol condition $\left( \frac{a}{p} \right) = -1$ and intersects these sets under two randomly chosen modulus shifts to ensure compatibility among multiple congruences. These are then resolved using the Chinese Remainder Theorem, producing a single residue class $x \bmod m$.

We then scan the arithmetic progression $x + i \cdot m$ to find the smallest candidate of a desired bit length such that the resulting “chain” of primes—$p_1,\, k_2(p_1 - 1) + 1,\, k_3(p_2 - 1) + 1, \dots$—are all prime. The final result is a large composite number $N = p_1 \cdot p_2 \cdot p_3$ that passes multiple rounds of strong pseudoprime tests, making it exceptionally difficult to distinguish from a true prime—a hallmark of Arnault’s construction.

For the complete, class-based SageMath version, see `src/arnaultmethod.sage`; the equivalent pure-Python version is available as `arnault.py`. What follows is a concise mathematical overview—you may skip it if you prefer to jump directly into the code.


## Fixed-Base Pseudoprimes: Bleichenbacher’s Construction

📄 *Reference*: **Daniel Bleichenbacher**, "Breaking a Cryptographic Protocol with Pseudoprimes".

### Korselt’s Criterion (for Carmichael Numbers)

A composite number $n$ is a *Carmichael number* if and only if:

1. $n$ is *square-free*.
2. For every prime divisor $p \mid n$, we have:

   $$
   p - 1 \mid n - 1
   $$

This condition ensures that FLT holds for all bases coprime to $n$, i.e., $a^{n-1} \equiv 1 \mod n$ ∀ $\gcd(a, n) = 1$.


### Erdős's Insight and Bleichenbacher’s Strategy

Erdős proposed constructing pseudoprimes by choosing an integer $M \in \mathbb{Z}$ with many divisors. Bleichenbacher builds on this to generate Carmichael numbers that are strong pseudoprimes to *specific fixed bases*.


1. Choose $M \in \mathbb{Z}$ with many divisors.
2. Let $R$ be the set of primes $r$ such that $r - 1 \mid M$.
3. Search for a subset $T \subseteq R$ such that:

   $$
   C = \prod_{r \in T} r \equiv 1 \pmod{M} \tag{1}
   $$

   Then $C$ satisfies Korselt’s Criterion ⇒ it is a *Carmichael number*.

* Each $r \in R$ satisfies $r - 1 \mid M$, and if the product of those $r$ is 1 modulo $M$, then:

  * $p - 1 \mid C - 1$ for all $p \mid C$ (since $r \in T \subset R$).
  * Thus, $C$ is Carmichael.


### Pseudoprimes for Fixed Bases

A Carmichael number $C$ is also a *strong pseudoprime* for base $a$ if:

* The order of $a \mod r$ is divisible by the *same power of 2* for all $r \mid C$

Bleichenbacher observed:

* If all $r \equiv 3 \mod 4$, then this uniformity condition is satisfied if:

  * $a$ is either a *quadratic residue modulo every $r$*, or
  * $a$ is a *non-residue modulo every $r$*

This means the order of $a \mod r$ will be uniformly even or uniformly odd across all prime factors.


The idea behind the algorithm aims to construct a *Carmichael number* $C$ such that:

* $C$ passes the *Miller–Rabin test* for all bases in a given set $A$,
* and satisfies *Korselt’s criterion*, ensuring it is a Carmichael number.

This means $C$ is a *strong pseudoprime* for every $a \in A$, and is thus a dangerous "liar" for fixed-base primality tests.

Now, we proceed with the functions: 

### `generate_M(a_list, prime_idx_bound, random_bound)`

* Constructs a highly divisible integer $M$.
* Starts with the product of small powers of bases in `a_list`.
* Then multiplies in additional small primes (from `next_prime`) to increase the number of divisors.
* The idea is: **more divisors ⇒ more candidate primes $r$ with $r - 1 \mid M$**.



### `find_set_R(a_list, M, r_low, r_high)`

* Finds a set of **primes $r$** such that:

  * $r - 1 \mid M$
  * For each base $a \in $ `a_list`, the **Legendre symbol** $\left(\frac{a}{r}\right) \in \{-1, 1\}$ (i.e., defined and meaningful)
* This ensures we can later control the quadratic residue status of $a \mod r$ — key for pseudoprimality under fixed bases.



### `find_subsets_T(R, M)`

* Tries to find a subset $T \subset R$ such that:

  $$
  \prod_{r \in T} r \equiv 1 \pmod{M}
  $$
* This satisfies *Korselt’s Criterion*, implying the product is a Carmichael number.
* Uses a *meet-in-the-middle strategy*:

  * Splits $R$ into two halves: $R_1, R_2$
  * Computes all subset products from $R_1$, storing their *modular inverses mod $M$*
  * Then for each subset of $R_2$, checks if its product modulo $M$ is equal to one of the precomputed inverses ⇒ if yes, combining the two subsets yields $\prod r \equiv 1 \mod M$



Below we explain the main script of Sagemath: 

```sagemath
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
```

If all conditions are satisfied, the resulting number \( C \):

- Is a *Carmichael number*,
- *Passes Miller–Rabin* for all bases in `a_list`,
- And thus serves as a *crafted counterexample* to fixed-base primality testing.

Once such a candidate is generated, use `testcarmichael.py` (found in the `src` folder) to validate its behavior across various tests.

The full implementation is available in the `src` folder. Run the code, extract the result, and verify it using the test script.

As we've seen, Bleichenbacher’s method demonstrates that *even fixed-base Miller–Rabin tests can be defeated* by carefully constructed Carmichael numbers. These pseudoprimes can be tailored to any chosen base set \( A \), exposing the *theoretical vulnerability* of fixed-base primality testing—even for cryptographically sized inputs.

### Wrap-Up: What We’ve Learned

In this final installment of our series, we’ve gone beyond classical and probabilistic primality tests to explore their **limits**:

* *Arnault’s method* constructs composite numbers that pass the Miller–Rabin test for multiple bases by chaining primes and enforcing quadratic residue constraints.
* *Bleichenbacher’s strategy* builds on Korselt’s Criterion to craft Carmichael numbers that fool even strong pseudoprime tests for fixed bases.
* These methods show that *probabilistic tests are not bulletproof*, especially when adversaries can tailor inputs.
* We’ve implemented both constructions in Python and SageMath, verified correctness, and demonstrated how these theoretical weaknesses can manifest in practice.

While Miller–Rabin is excellent for general use, *relying on fixed bases* opens the door to sophisticated attacks using crafted pseudoprimes. Cryptographic systems should account for this by:

* Using random bases,
* Running multiple iterations,
* Or applying deterministic algorithms like AKS when absolute certainty is required.

 In the distant future, our journey will lead us even further—toward deterministic primality proofs like AKS and advanced techniques involving elliptic curves. But before we get there, we’ll need to sharpen our mathematical toolkit with more *mathematricks* and number-theoretic depth. Until then, keep exploring, experimenting, and questioning what it *really means* for a number to be prime.
