- [Chinese Remainder Theorem (CRT)](#chinese-remainder-theorem-crt)
    - [Preliminary Lemma](#preliminary-lemma)
    - [Chinese Remainder Theorem](#chinese-remainder-theorem)
  - [Applications and Use](#applications-and-use)
  - [A simple example:](#a-simple-example)
  - [Custom Implementation in Python](#custom-implementation-in-python)
    - [Using SageMath](#using-sagemath)
  - [Summary and Future Applications](#summary-and-future-applications)


# Chinese Remainder Theorem (CRT)




---

> "We have a number of things, but we do not know exactly how many.  
> If we count them by threes we have two left over.  
> If we count them by fives we have three left over.  
> If we count them by sevens we have two left over.  
> How many things are there?"  
> — *Sunzi, Sunzi Suanjing* (3rd–5th century)

### Preliminary Lemma

Let \( n \in \mathbb{N}^* \) and \( a, b \in \mathbb{Z} \). If \( d = \gcd(a, n) \), and \( d \mid b \), then the congruence:
\[
ax \equiv b \pmod{n}
\]
has exactly \( d \) solutions in \( \{0, 1, \ldots, n-1\} \).


### Chinese Remainder Theorem

Let \( m_1, m_2, \ldots, m_k \in \mathbb{N}^* \) be pairwise coprime, and let \( a_1, a_2, \ldots, a_k \in \mathbb{Z} \). Then the system:
\[
\begin{aligned}
x &\equiv a_1 \pmod{m_1} \\
x &\equiv a_2 \pmod{m_2} \\
&\vdots \\
x &\equiv a_k \pmod{m_k}
\end{aligned}
\]
has a unique solution modulo \( M = m_1 m_2 \cdots m_k \).

**Special case**: *If \( \gcd(n_1, n_2) = 1 \), and \( x \equiv a \pmod{n_1} \), \( x \equiv a \pmod{n_2} \), then*:
\[
x \equiv a \pmod{n_1 n_2}
\]

---

## Applications and Use

CRT plays a foundational role in number theory and computer science. It is used in:

- Modular exponentiation (e.g., RSA optimizations)
- Finite field arithmetic
- Secret sharing and threshold cryptography
- Symbolic computation
- Fast Fourier Transform over modular rings

---

## A simple example: 

Find \( x \in \mathbb{Z} \) such that:
\[
\begin{aligned}
x &\equiv 5 \pmod{13} \\
x &\equiv 8 \pmod{17} \\
x &\equiv 15 \pmod{29}
\end{aligned}
\]


We apply the CRT using:
- \( N = 13 \cdot 17 \cdot 29 = 6409 \)
- \( N_i = N / n_i \)
- \( y_i = N_i^{-1} \mod n_i \)
- Final solution:
  \[
  x \equiv \sum_{i=0}^{2} b_i \cdot N_i \cdot y_i \pmod{N}
  \]



| \( i \) | \( b_i \) | \( n_i \) | \( N_i \) | \( y_i \equiv N_i^{-1} \mod n_i \) | \( b_i N_i y_i \) |
|--------:|----------:|----------:|----------:|------------------------------------:|------------------:|
|   0     |     5     |    13     |    493    |              12                     |      29580        |
|   1     |     8     |    17     |    377    |               6                     |      18096        |
|   2     |    15     |    29     |    221    |              21                     |      69615        |


\[
x \equiv (29580 + 18096 + 69615) \mod 6409 = 117291 \mod 6409 = \boxed{1929}
\]


The unique solution is:
\[
x \equiv 1929 \pmod{6409}
\]

---

## Custom Implementation in Python

We implement CRT using a reduction of congruences one by one:

```python
from Crypto.Util.number import inverse

def solve_simple_eq(a, b, c, p):
    """
    Solves a + bx ≡ c mod p
    Equivalent to: x = (c - a) * b^{-1} mod p
    """
    return ((c - a) * inverse(b, p)) % p

def crt(a_list, m_list):
    a = 0  # accumulated solution
    m = 1  # accumulated modulus
    for i in range(len(m_list)):
        x = solve_simple_eq(a, m, a_list[i], m_list[i])
        a = a + m * x
        m = m * m_list[i]
    return a % m, m

crt([2, 3, 2], [3, 5, 7])
# Output: (23, 105)

crt([5, 5], [7, 13])
# Output: (5, 91)
```

### Using SageMath

```sage
crt([2,3,2],[3,5,7])
# Output: 23
```

---

## Summary and Future Applications

We presented the *simplest form* of the Chinese Remainder Theorem, both theoretically and practically. The CRT is a fundamental tool that will reappear frequently in our advanced topics such as:

- Cryptographic algorithms (RSA, Paillier, ElGamal)
- Computation in finite fields \( \mathbb{F}_p \) and rings \( \mathbb{Z}/n\mathbb{Z} \)
- Polynomial interpolation
- Lattice-based and homomorphic encryption
