- [Euler’s Totient Function ( \\phi(n) )](#eulers-totient-function--phin-)
  - [Order of an Element in ( \\mathbb{Z}\_n^\* )](#order-of-an-element-in--mathbbz_n-)
  - [Properties and Identities](#properties-and-identities)
    - [Prime Decomposition Formula](#prime-decomposition-formula)
  - [Computational Examples](#computational-examples)
    - [Naive Implementation in SageMath](#naive-implementation-in-sagemath)
    - [Efficient Built-in Usage](#efficient-built-in-usage)
      - [SageMath](#sagemath)
      - [Python (via SymPy)](#python-via-sympy)
  - [Wrap-up](#wrap-up)

---
# Euler’s Totient Function \( \phi(n) \)

Euler’s totient function \( \phi(n) \), also known as Euler’s \(\phi\)-function, plays a central role in number theory and cryptography. It counts the number of positive integers less than or equal to \( n \) that are *coprime* to \( n \), i.e., share no common divisors with \( n \) other than 1. Euler introduced this function in 1760. Although he originally used \( \pi(n) \), the now standard notation \( \phi(n) \) was adopted by Gauss in his *Disquisitiones Arithmeticae*. Today, it is also referred to as the *Euler totient function*. 
Below we define the group of units of $ \mathbb{Z}_n$: 

>Let \( \mathbb{Z}_n^* \) denote the set of invertible elements modulo \( n \), i.e., the residue classes \([x]_n\) such that \( \gcd(x, n) = 1 \). This set forms a group under multiplication modulo \( n \), known as the **group of units of \( \mathbb{Z}_n \)**. The number of elements in this group is precisely:
>
>\[
>\phi(n) = \#\left\{ a \in \mathbb{Z} : 1 \leq a \leq n,\, \gcd(a,n) = 1 \right\}
>\]

## Order of an Element in \( \mathbb{Z}_n^* \)

If \( x \in \mathbb{Z}_n^* \), the **order** of \( x \) modulo \( n \) is the smallest positive integer \( m \) such that:

\[
x^m \equiv 1 \pmod{n}
\]

This definition is well-posed because the powers of \( x \mod n \) must eventually repeat (finitely many residues), and if \( \gcd(x, n) = 1 \), cancellation is permitted modulo \( n \), ensuring that such an \( m \) exists.

*Example in Sagemath:*

```sage
R = Integers(10)
a = R(3)
a.multiplicative_order()  # Output: 4
[a^i for i in range(15)]
```

This reveals the periodicity \( 3^4 \equiv 1 \mod 10 \).

*Simple Examples:*

\[
\begin{aligned}
\phi(1) &= 1 \quad &\text{(by convention)} \\
\phi(2) &= 1 \quad &\text{(only 1 is coprime to 2)} \\
\phi(5) &= 4 \quad &\text{(1, 2, 3, 4)} \\
\phi(12) &= 4 \quad &\text{(1, 5, 7, 11)} \\
\phi(13) &= 12 \quad &\text{(since 13 is prime)} \\
\phi(14) &= 6 \quad &\text{(1, 3, 5, 9, 11, 13)}
\end{aligned}
\]

---

## Properties and Identities

- \( \phi(p) = p - 1 \) for any prime \( p \)
- \( \phi(p^a) = p^a - p^{a - 1} = p^{a - 1}(p - 1) \)
- \( \phi \) is **multiplicative**:  
  If \( \gcd(m, n) = 1 \), then:
  \[
  \phi(mn) = \phi(m) \cdot \phi(n)
  \]

### Prime Decomposition Formula

If \( n = \prod_{i=1}^r p_i^{a_i} \), then:
\[
\phi(n) = n \prod_{i=1}^r \left( 1 - \frac{1}{p_i} \right)
\]


*Example:* Compute \( \phi(360) \). The prime factorization is:
\[
360 = 2^3 \cdot 3^2 \cdot 5
\]
\[
\phi(360) = 360 \left(1 - \frac{1}{2} \right)\left(1 - \frac{1}{3} \right)\left(1 - \frac{1}{5} \right)
= 360 \cdot \frac{1}{2} \cdot \frac{2}{3} \cdot \frac{4}{5} = \boxed{96}
\]

With a bigger number now: 

*Example:* Calculate \( \phi(304920) \):

Let:
\[
304920 = 2^3 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11^2
\]

Then:
\[
\phi(304920) = 304920 \left( \frac{1}{2} \right)\left( \frac{2}{3} \right)\left( \frac{4}{5} \right)\left( \frac{6}{7} \right)\left( \frac{10}{11} \right) = \boxed{63360}
\]

---

Some more advanced mumber theoretic properties that will be useful in the future:

- \( \phi(n) \) is even for all \( n > 2 \)
- For prime \( p \), \( \phi(p^k) = p^k - p^{k-1} \)
- For large \( n \), the average of the first \( n \) values of \( \phi \) satisfies:
  \[
  \frac{1}{n} \sum_{k=1}^n \phi(k) \approx \frac{6n}{\pi^2}
  \]

*Liouville’s Identity (1857):*

\[
\frac{\zeta(s - 1)}{\zeta(s)} = \sum_{n=1}^\infty \frac{\phi(n)}{n^s} \quad \text{for } s > 1
\]

This expresses a Dirichlet generating function involving the Riemann zeta function.

*Asymptotic Bounds:*

\[
\frac{\sqrt{n}}{2} < \phi(n) \leq \frac{n}{e^\gamma \ln(\ln(n))}, \quad \text{for large } n
\]
where \( \gamma \approx 0.5772 \) is the *Euler–Mascheroni constant*.

---

Interesting applications and open questions regarding the euler function: 

- In RSA, decryption requires computing modular inverses via \( \phi(n) \)
- *Carmichael (1922):* Is \( \phi(m) = \phi(n) \) for \( m \neq n \)? (Yes, for large \( m \), but first such \( m > 10^{10^7} \))
- *Lehmer’s Question (1932):* Does \( \phi(n) \mid n - 1 \Rightarrow n \) is prime?

---

## Computational Examples

In practice, Euler’s totient function can be computed either through its prime factorization formula or using built-in functions in computational environments such as **SageMath** and **Python**.

### Naive Implementation in SageMath

A direct way to compute \( \phi(n) \) is by counting the number of integers \( i \) in the range \( 1 \leq i < n \) such that \( \gcd(i, n) = 1 \). For each such \( i \), we may also display its inverse modulo \( n \), which exists precisely when \( \gcd(i, n) = 1 \):

```sage
n = 100000
k = 0
for i in range(n):
    if gcd(i, n) == 1:
        print("{:2} with inverse {:}".format(i, mod(1/i, n)))
        k += 1
print("Number of invertible elements: {:}".format(k))

# Cross-verify using the built-in euler_phi function
print("Now using euler_phi: {:}".format(euler_phi(n)))
```

This script not only counts the invertible elements in \( \mathbb{Z}_n \), but also lists their modular inverses, showcasing the group structure of \( \mathbb{Z}_n^* \). The final count of such elements is returned by Euler’s \(\phi\)-function.


### Efficient Built-in Usage

#### SageMath

SageMath includes a highly optimized built-in function `euler_phi` as we mentioned earlier, that directly evaluates the Euler totient function:

```sage
euler_phi(304920)  # Output: 63360
```

This uses the multiplicative formula:
\[
\phi(n) = n \prod_{p \mid n} \left(1 - \frac{1}{p}\right)
\]

#### Python (via SymPy)

Python’s `sympy` library provides the `totient()` function to evaluate \( \phi(n) \):

```python
from sympy import totient
print(totient(360))  # Output: 96
```

Note that, while a naive approach offers transparency and insight into the structure of \( \mathbb{Z}_n^* \), built-in implementations should be preferred in cryptographic and algorithmic contexts for performance and scalability.

## Wrap-up

Euler’s totient function \( \phi(n) \) counts the number of integers less than or equal to \( n \) that are coprime to \( n \). Despite its simple definition, it holds deep arithmetic structure and lies at the heart of the multiplicative group \( \mathbb{Z}_n^* \), where many cryptographic operations are performed.

Its role is central in number theory and essential for modern cryptographic protocols such as RSA, ElGamal, and primality testing. Understanding how to compute it efficiently — and recognizing when and why it's used — will be crucial throughout our study of cryptography.


> *"Euler gave us the key, centuries before the lock was even built."*
