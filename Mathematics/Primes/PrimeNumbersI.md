- [Prime Numbers (Part I)](#prime-numbers-part-i)
  - [Primes and Factorization](#primes-and-factorization)
    - [The Fundamental Theorem of Arithmetic](#the-fundamental-theorem-of-arithmetic)
    - [Proof of the Fundamental Theorem of Arithmetic](#proof-of-the-fundamental-theorem-of-arithmetic)
    - [Consequences of Unique Factorization](#consequences-of-unique-factorization)
  - [Basic Properties of Primes](#basic-properties-of-primes)
    - [Coprimality with Primes](#coprimality-with-primes)
    - [Divisibility and Coprimality with Primes](#divisibility-and-coprimality-with-primes)
    - [Prime Divisibility of Products](#prime-divisibility-of-products)
    - [Converse of Prime Divisibility](#converse-of-prime-divisibility)
    - [Divisibility in Multiple Factors](#divisibility-in-multiple-factors)
  - [Infinitude and Structure of the Primes](#infinitude-and-structure-of-the-primes)
    - [Gaps Between Primes](#gaps-between-primes)
    - [The ( p )-adic Valuation](#the--p--adic-valuation)
  - [Prime Number Theorem](#prime-number-theorem)
    - [Euler's Totient Function](#eulers-totient-function)
  - [Generating Large Primes](#generating-large-primes)
    - [Using PyCryptodome in Python](#using-pycryptodome-in-python)
    - [Using SageMath](#using-sagemath)
  - [Numbers Factor as Products of Primes](#numbers-factor-as-products-of-primes)
    - [Computational Factoring](#computational-factoring)
  - [A prelude with some Factoring Challenges and Cryptographic Relevance](#a-prelude-with-some-factoring-challenges-and-cryptographic-relevance)
  - [Wrap-up](#wrap-up)

# Prime Numbers (Part I)

Every positive integer can be written uniquely as a product of prime numbers. For instance:

\[
100 = 2^2 \cdot 5^2.
\]

This fundamental property, while intuitively simple, is surprisingly nontrivial to prove. Moreover, actually *finding* the prime factorization of large numbers, such as integers with several hundred or thousand digits, remains computationally infeasible with current technology. This computational difficulty is the foundation for widely used applications in modern cryptography, including online transactions.

Since prime numbers are the basic building blocks of the integers, it is natural to study their distribution among the natural numbers. Don Zagier captured this duality in the behavior of primes:


*There are two facts about the distribution of prime numbers. The first is that they are the most arbitrary and ornery objects studied by mathematicians: they grow like weeds among the natural numbers, seeming to obey no other law than that of chance, and nobody can predict where the next one will sprout. The second fact is even more astonishing, for it states just the opposite: that the prime numbers exhibit stunning regularity, that there are laws governing their behavior, and that they obey these laws with almost military precision.*


The famous *Riemann Hypothesis* postulates a highly precise description of the distribution of prime numbers and remains the most important unsolved problem in number theory.

We will try to lay the foundations for the study of prime numbers by intertwining the themes of *unique factorization*, *integer factorization algorithms*, and the *distribution of primes*. We rigorously establish that every positive integer admits a prime factorization and discuss the challenges involved in factoring large integers. Subsequently, we present classical results concerning primes, including Euclid’s proof of the infinitude of primes and a discussion of the largest known primes. Eventually we will work towards the *Prime Number Theorem* and the *Riemann Hypothesis* as key results describing the asymptotic behavior of prime numbers.

The principal objective of is to develop the *Fundamental Theorem of Arithmetic* (also known as the *Unique Factorization Theorem*), which asserts:

> Every integer \( n \geq 2 \) can be expressed uniquely, up to the order of the factors, as a product of prime numbers.

Explicit examples of prime factorizations include:

\[
36 = 2^2 \cdot 3^2, \qquad 986 = 2 \cdot 17 \cdot 29, \qquad 10001 = 73 \cdot 137.
\]

---

## Primes and Factorization

Remember what we said already about divisibility: 

**(Divides):** Let \( a, b \in \mathbb{Z} \). We say that \( a \) *divides* \( b \), written \( a \mid b \), if there exists \( c \in \mathbb{Z} \) such that \( b = ac \).  
Otherwise, we write \( a \nmid b \).

For example, \( 2 \mid 6 \) and \( -3 \mid 15 \), but \( 3 \nmid 7 \).  
Note that every integer divides \( 0 \), and \( 0 \) divides only itself.


**(Prime and Composite):** An integer \( n > 1 \) is:

- *Prime* if its only positive divisors are \( 1 \) and \( n \).
- *Composite* if it is not prime.

Prime numbers are often referred to as the *building blocks* of the integers. However, when generalizing to more abstract algebraic structures, it becomes necessary to distinguish between two closely related notions: *prime elements* and *irreducible elements*.


**(Prime, Irreducible, and Composite Elements):** Let \( z \geq 2 \) be an integer. Then:

- \( z \) is *prime* if, whenever \( z \mid ab \), then \( z \mid a \) or \( z \mid b \).
- \( z \) is *irreducible* if its only positive divisors are \( 1 \) and \( z \).
- \( z \) is *composite* if there exist \( a, b \in \mathbb{N} \) such that \( z = ab \) with \( 2 \leq a, b < z \).

In \( \mathbb{Z} \), the notions of *prime* and *irreducible* coincide. However, in more general rings, these concepts may differ.  

For instance, in the ring \( \mathbb{Z}[\sqrt{10}] \), the number \( 6 \) admits two distinct factorizations:

\[
6 = 2 \times 3 = (\sqrt{10} - 2)(\sqrt{10} + 2),
\]
where \( 2 \) is irreducible but not prime.  
This highlights that *unique factorization* fails in some rings outside \( \mathbb{Z} \).

A more striking example is found in \( \mathbb{Z}[\sqrt{-5}] \), defined as:

\[
\mathbb{Z}[\sqrt{-5}] = \{ a + b\sqrt{-5} : a, b \in \mathbb{Z} \}.
\]

This ring is closed under addition and multiplication and admits a *norm map*:

\[
N(a + b\sqrt{-5}) = a^2 + 5b^2,
\]
which satisfies the multiplicative property \( N(\alpha\beta) = N(\alpha)N(\beta) \).

In \( \mathbb{Z}[\sqrt{-5}] \), the number \( 6 \) factors in two essentially different ways:

\[
6 = 2 \times 3 = (1+\sqrt{-5})(1-\sqrt{-5}),
\]
despite all the elements involved being irreducible.  
Thus, *unique factorization* fails in this ring as well.

The degree to which unique factorization fails in a ring is quantified by an important invariant called the *class number*, which we will discuss later.

Some basic examples to keep in mind:

- The number \( 1 \) is neither prime nor composite.
- The first few primes are:

\[
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, \ldots
\]

- The first few composites are:

\[
4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, \ldots
\]

>Every composite integer is divisible by an irreducible.

**Theorem (Euclid's Lemma):** If \( p \) is prime and \( p \mid ab \), then \( p \mid a \) or \( p \mid b \). More generally, if \( p \mid a_1 \cdots a_n \), then \( p \) divides at least one of the factors \( a_i \).

*Proof Sketch:* If \( p \nmid a \), then \(\gcd(p,a) = 1\), and thus \( p \mid b \) by properties of greatest common divisors. The general case follows by induction.

**(Perfect Squares and Square-Free Numbers)**:
- A positive integer \( a \) is a **perfect square** if \( a = n^2 \) for some \( n \in \mathbb{Z} \).  
  In the prime factorization of a perfect square, every exponent is even.

- A number \( a \) is **square-free** if no prime square divides \( a \).  
  Equivalently, all exponents in its prime factorization are \( 0 \) or \( 1 \).


### The Fundamental Theorem of Arithmetic

We now state one of the cornerstones of number theory.

**Theorem (Fundamental Theorem of Arithmetic).**  
Every integer \( z \) is either \( 0 \), \( \pm 1 \), or can be uniquely expressed (up to order and units \( \pm 1 \)) as:

\[
z = u \cdot p_1^{\mu_1} \cdots p_n^{\mu_n},
\]
where:

- \( u = \pm 1 \),
- \( p_1 < p_2 < \cdots < p_n \) are primes,
- \( \mu_i \in \mathbb{N} \) for each \( i \).

Thus, every integer greater than \( 1 \) admits a unique factorization into primes.

The *existence* part follows by an iterative process:  
- If \( n \) is prime, it is already expressed as a prime power.
- Otherwise, \( n = n_1 n_2 \), where \( 1 < n_1, n_2 < n \).
- If either \( n_1 \) or \( n_2 \) is composite, they can be further factored.

Since each new factor is strictly smaller than the previous number and greater than \( 1 \), the process must terminate, resulting in a product of primes.

Thus, for any \( n > 1 \), we ultimately have:

\[
n = p_1^{a_1} p_2^{a_2} \cdots p_r^{a_r},
\]
where the \( p_i \) are distinct primes and \( a_i > 0 \).


**Remark:** The Fundamental Theorem of Arithmetic is more delicate than it first appears. Unique factorization can fail in more general settings.

**Theorem (Existence of Prime Factorization):** Every integer \( z \geq 2 \) can be expressed as a product of irreducibles.

The existence part of the Fundamental Theorem of Arithmetic follows by successively factoring composite numbers until only irreducibles remain.

**Lemma.**: In the integers \( \mathbb{Z} \), primes and irreducibles are identical.

This equivalence is crucial, allowing us to equate "product of irreducibles" with "product of primes."

For example, in the ring:

\[
\mathbb{Z}[\sqrt{-5}] = \{a + b\sqrt{-5} : a, b \in \mathbb{Z}\},
\]
the number \( 6 \) admits two distinct factorizations into irreducibles:

\[
6 = 2 \times 3 = (1+\sqrt{-5})(1-\sqrt{-5}),
\]
demonstrating that *unique factorization* does not always hold outside of \( \mathbb{Z} \).


To compute primes in a range we gonna use Sagemath:

```sage
prime_range(10, 50)
# Output: [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

To list composites:

```sage
[n for n in range(10, 30) if not is_prime(n)]
# Output: [10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28]
```

### Proof of the Fundamental Theorem of Arithmetic

Suppose \( n > 1 \) has two prime factorizations:

\[
n = p_1 p_2 \cdots p_d = q_1 q_2 \cdots q_m.
\]

Using Euclid's Lemma:

- \( p_1 \) divides \( q_1 q_2 \cdots q_m \),
- Hence \( p_1 \) divides some \( q_i \), and because \( q_i \) is prime, \( p_1 = q_i \),
- Cancel \( p_1 \) and \( q_i \) from both sides and continue by induction.

Thus, the two factorizations consist of exactly the same primes, completing the proof.

### Consequences of Unique Factorization

**Corollary:** Suppose:

\[
a = p_1^{\mu_1} \cdots p_n^{\mu_n}, \quad b = p_1^{\nu_1} \cdots p_n^{\nu_n}
\]
are the unique prime factorizations of \( a \) and \( b \). Then:

1. \( b \mid a \) if and only if \( \nu_i \leq \mu_i \) for all \( i \).
2. \[
\gcd(a, b) = p_1^{\min(\mu_1, \nu_1)} \cdots p_n^{\min(\mu_n, \nu_n)}.
\]
3. \( a \) is a perfect square if and only if every \( \mu_i \) is even.
4. \( a^2 \mid b^2 \) implies \( a \mid b \).
5. If \( ab \) is a perfect square and \( \gcd(a, b) = 1 \), then both \( a \) and \( b \) are perfect squares.

---

## Basic Properties of Primes

### Coprimality with Primes

**Proposition:** Let \( p \) be a prime. Then for each \( i \in \{1, 2, \ldots, p-1\} \), we have \(\gcd(i, p) = 1\); that is, each such \( i \) is coprime to \( p \).

**Proof.**  
Let \( i \in \{1, 2, \ldots, p-1\} \).  
Since \( 1 \leq i < p \), \( i \neq 0 \), and \( p \) is a prime number, the only positive divisors of \( p \) are \( 1 \) and \( p \) itself.

Suppose \( d = \gcd(i, p) \). Then \( d \) divides both \( i \) and \( p \).  
Since \( d \) divides \( p \) and \( p \) is prime, \( d \) must be either \( 1 \) or \( p \).  
But \( d \leq i < p \), hence \( d \neq p \), so \( d = 1 \).  
Thus, \( \gcd(i, p) = 1 \), and \( i \) is coprime to \( p \).  \(\blacksquare\)



**Remark:** This property characterizes primes: if \( p > 1 \) and every \( i \in \{1, \ldots, p-1\} \) is coprime to \( p \), then \( p \) must be prime.


### Divisibility and Coprimality with Primes

**Proposition:** Let \( p \) be a prime, and let \( a \in \mathbb{Z} \).  
Then either \( p \mid a \) or \( \gcd(p, a) = 1 \).

**Proof.**  
Assume, for contradiction, that neither \( p \mid a \) nor \( \gcd(p, a) = 1 \).

Since \( p \) is prime, its only positive divisors are \( 1 \) and \( p \).  
As \( \gcd(p, a) \) divides \( p \) and \( \gcd(p, a) \neq p \) (because \( p \nmid a \)), we must have \( \gcd(p, a) = 1 \).  
This contradicts the assumption that \( \gcd(p, a) \neq 1 \).

Thus, either \( p \mid a \) or \( \gcd(p, a) = 1 \).  \(\blacksquare\)



**Remark:** The converse is also true: if for all integers \( a \), either \( p \mid a \) or \( \gcd(p,a) = 1 \), then \( p \) must be prime.


### Prime Divisibility of Products

**Theorem:** Let \( p \) be a prime, and let \( a, b \in \mathbb{Z} \).  
If \( p \mid ab \), then \( p \mid a \) or \( p \mid b \).

**Proof.**  
Assume \( p \mid ab \) but \( p \nmid a \).  
By the previous proposition, \( \gcd(p,a) = 1 \).  
Thus, by basic properties of divisibility, \( p \mid b \).  \(\blacksquare\)

### Converse of Prime Divisibility

**Theorem (Converse):** Let \( p > 1 \) be an integer. If for all \( a, b \in \mathbb{Z} \), the condition \( p \mid ab \) implies \( p \mid a \) or \( p \mid b \), then \( p \) is prime.

**Proof.**  
Assume \( p \) is not prime.  
Then \( p = ab \) for some \( 1 < a, b < p \).  
Clearly \( p \mid ab \), but \( p \nmid a \) and \( p \nmid b \), contradicting the given property.  
Thus, \( p \) must be prime. \(\blacksquare\) 



### Divisibility in Multiple Factors

**Proposition:** Let \( p \) be a prime, and let \( a_1, a_2, \ldots, a_k \in \mathbb{Z} \).  
If \( p \mid a_1 a_2 \cdots a_k \), then \( p \mid a_i \) for some \( i \in \{1,2,\ldots,k\} \).

**Proof Sketch.**  
The case \( k = 2 \) follows by the prime divisibility theorem.  
The general case follows by induction on \( k \).

So far, we have established several fundamental properties of primes:

- Every integer less than a prime is coprime to it.
- If a prime divides a product, it divides at least one factor.
- The converse holds: primes are characterized by this divisibility property.
- Prime divisibility extends naturally to products of multiple integers.

These results are foundational for the development of modular arithmetic, Euler's theorem, and many deeper theorems in number theory.


## Infinitude and Structure of the Primes


**Theorem (Euclid).**: There are infinitely many primes.

This fundamental result, first proven by Euclid around 300 BCE, guarantees that primes never "run out." 

**Corollary:** The uniqueness part of the Fundamental Theorem of Arithmetic follows from the equivalence of primes and irreducibles.

**Proposition.**: There are infinitely many primes of the form \( 4n-1 \).

This extends Euclid’s idea into special residue classes.

### Gaps Between Primes

**Proposition:** For any \( k \in \mathbb{N} \), there exist \( k \) consecutive composite numbers.

*Idea:* Consider \( (k+1)! + 2, (k+1)! + 3, \dotsc, (k+1)! + (k+1) \), each divisible by \( 2, 3, \dotsc, k+1 \) respectively.

### The \( p \)-adic Valuation

**Definition (Valuation):** Let \( p \) be a prime and \( n \in \mathbb{N} \).  
The \( p \)-adic valuation of \( n \), denoted \( v_p(n) \), is the largest \( k \in \mathbb{N} \cup \{0\} \) such that \( p^k \mid n \).

**Lemma:** For all \( m, n \in \mathbb{N} \) and prime \( p \):

\[
v_p(mn) = v_p(m) + v_p(n).
\]

---

## Prime Number Theorem

Let \( \pi(x) \) denote the number of prime numbers less than or equal to \( x \). Then:

\[
\lim_{x \to \infty} \frac{\pi(x)}{x / \ln x} = 1.
\]

In words:  
> For large values of \( x \), the number of primes up to \( x \) is approximately \( \frac{x}{\ln x} \).

Thus, primes become less frequent as numbers grow, but in a very precise manner described asymptotically by \( \frac{x}{\ln x} \).

For further reference, see [MathWorld: Prime Number Theorem](https://mathworld.wolfram.com/PrimeNumberTheorem.html).

We can numerically estimate the number of primes between two large numbers using the above approximation in Python: 

```python
import numpy as np

n1 = 100000
n2 = 1000000

def expected_num_primes(x):
    return x / np.log(x)

print(f"Expected number of primes between {n1} and {n2} is {expected_num_primes(n2) - expected_num_primes(n1)}")
```


### Euler's Totient Function

We recall that the *Euler totient function* \( \phi(n) \) counts the number of positive integers less than or equal to \( n \) that are coprime to \( n \).

\[
\phi(n) = \#\{ 1 \leq k \leq n : \gcd(k, n) = 1 \}.
\]

Some fundamental properties: 

- If \( p \) is a prime number, then:

\[
\boxed{\phi(p) = p - 1}.
\]

- **Multiplicative Property:**  
If \( \gcd(m,n) = 1 \), then:

\[
\phi(mn) = \phi(m) \cdot \phi(n).
\]

- **Formula from Prime Factorization:**  
If:

\[
n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}
\]
is the prime factorization of \( n \), then:

\[
\phi(n) = n \left( 1 - \frac{1}{p_1} \right) \left( 1 - \frac{1}{p_2} \right) \cdots \left( 1 - \frac{1}{p_k} \right).
\]

For further details, see `EulerPhi.md` and [Wikipedia: Euler's Totient Function](https://en.wikipedia.org/wiki/Euler%27s_totient_function).

---

## Generating Large Primes

### Using PyCryptodome in Python

The `PyCryptodome` library provides a simple interface to generate large prime numbers of specified bit length.

```python
from Crypto.Util.number import getPrime

# Generate a 128-bit prime
p = getPrime(128)
print(p)  # Output: A 128-bit prime number
print(p.bit_length())  # Output: 128

# Generate a 768-bit prime
p = getPrime(768)
print(p)  # Output: A 768-bit prime number
print(p.bit_length())  # Output: 768
```

### Using SageMath

In SageMath, generating primes of a given size is straightforward:

```sage
# Generate a random prime in the range [2^127, 2^128]
p = random_prime(2^128, lbound=2^127)
print(p)  # Output: A prime number within the specified range

# Check the type of the generated prime
print(type(p))  # Output: <class 'sage.rings.integer.Integer'>

# Verify the number of bits
print(p.nbits())  # Output: 128
```

---


## Numbers Factor as Products of Primes

Since we have now established the essential theoretical foundations, our next objective is to discuss additional aspects related to integer factorization. It is important to note that a comprehensive analysis of factorization methods will be carried out later. At this stage, we will restrict ourselves to stating the basic principles, especially since we have already introduced the Fundamental Theorem of Arithmetic.

As a motivating example, consider the integer \( n = 1275 \).

Since the sum of its digits is divisible by \( 3 \), it follows that \( 3 \mid 1275 \). Dividing by \( 3 \) yields:
\[
1275 = 3 \times 425.
\]
Observing that \( 425 \) ends in \( 5 \), we conclude that \( 5 \mid 425 \), and thus:
\[
1275 = 3 \times 5 \times 85.
\]
Repeating the process by dividing \( 85 \) again by \( 5 \), we obtain:
\[
1275 = 3 \times 5^2 \times 17,
\]
where \( 17 \) is prime. Hence, the prime factorization of \( 1275 \) is complete.

This procedure reflects the two general principles about the existence of prime factorization and divisor we talked above.

It is notable that different sequences of divisions still lead to the same prime factorization. For instance:
\[
1275 = 5 \times 255, \quad 255 = 5 \times 51, \quad 51 = 17 \times 3,
\]
thus confirming once again:
\[
1275 = 3 \times 5^2 \times 17.
\]

This consistency suggests that prime factorizations are unique up to *ordering*.


### Computational Factoring

The `factor` command in SageMath factors integers into primes:

```python
sage: factor(1275)
3 * 5^2 * 17

sage: factor(2007)
3^2 * 223

sage: factor(31415926535898)
2 * 3 * 53 * 73 * 2531 * 534697
```

An algorithm is said to operate in *polynomial time* if its running time is bounded above by a polynomial function of \( \log_{10}(n) \), where \( n \) is the size of the input. That is, the complexity is measured in terms of the number of digits of \( n \). A more detailed study of complexity theory will be presented in a subsequent analysis.

At present, it remains an open question whether a polynomial-time algorithm for integer factorization exists on classical computers. However, Peter Shor developed a groundbreaking polynomial-time algorithm for factoring integers on quantum computers (see [Shor's algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)). In 2001, researchers at IBM successfully implemented Shor’s algorithm to factor the number \( 15 \) on a prototype quantum computer.

---

## A prelude with some Factoring Challenges and Cryptographic Relevance

Many cryptosystems depend on the difficulty of factoring large integers. To bolster confidence in the hardness of factoring, prizes have been offered for factoring challenge numbers.

For example, until 2003, a \$10,000 bounty was offered for factoring the 174-digit number known as *RSA-576*:

\[
1881988129206079638386972394616504398071635633794173827007\ldots
\]

This number was eventually factored using sophisticated algorithms. Previous challenges, such as *RSA-155* (a 155-digit number), were also successfully factored, confirming the effectiveness of state-of-the-art techniques like the *Number Field Sieve*.

The current open challenge (RSA-704) involves factoring a 704-bit integer, with a \$30,000 prize:

\[
74037563479561712828046796097429573142593188889231289084936232\ldots
\]

Using SageMath, it is easy to verify that RSA-704 is indeed composite:

```python
sage: n = 7403756347956171282804679609742957314259318888... (number continued)
sage: n.is_prime()
False
```

There exist several algorithms for integer factorization. However, determining the optimal method for factoring integers remains an open and profound problem in both mathematics and computer science. A thorough understanding of factorization techniques is essential, especially considering their pivotal role in modern cryptography.

The tasks of factoring large integers and efficiently testing the primality of large numbers are both intrinsically difficult. These subjects require distinct and detailed treatment, as they form the foundation upon which many cryptographic protocols are built. 

Accordingly, a careful and systematic study of integer factorization methods and primality testing algorithms will be indispensable for the continuation of our exploration into cryptographic systems.

---

## Wrap-up

In this part, we have developed the fundamental notions regarding prime numbers and integer factorizations:

- We introduced the concepts of divisibility, primes, composites and square-free numbers.
- We proved the *Fundamental Theorem of Arithmetic*, establishing that every integer greater than one can be factored uniquely into primes.
- We highlighted the special role of primes in modular arithmetic, including basic results such as *Euclid's Lemma* and the behavior of primes in congruences.
- We briefly introduced the computational difficulty of integer factorization and primality testing, emphasizing their critical importance to modern cryptography.
- We mentioned the distinction between classical and quantum approaches to factoring, noting the revolutionary impact of Shor’s algorithm on the theory of quantum computation.

This foundational material prepares us for the next stages of study, where these principles will be applied extensively to develop cryptographic schemes, analyze security assumptions, and understand modern public-key infrastructures.






