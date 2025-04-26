## Table of Contents

- [Number Theory (Part 2)](#number-theory-part-2)
  - [Modular Arithmetic and Computation](#modular-arithmetic-and-computation)
    - [Python’s `%` Operator](#pythons--operator)
    - [Reduction at Intermediate Steps](#reduction-at-intermediate-steps)
    - [Example: Computing ( 3^{999} \\mod 1000 )](#example-computing--3999-mod-1000-)
  - [Residues](#residues)
  - [Residue Classes](#residue-classes)
    - [Congruence and Least Nonnegative Residues](#congruence-and-least-nonnegative-residues)
    - [Example: Residue Classes Modulo 4](#example-residue-classes-modulo-4)
    - [Complete Residue System](#complete-residue-system)
  - [General Structure: Residue Classes Modulo ( n )](#general-structure-residue-classes-modulo--n-)
    - [Example: Residue Classes Modulo 5](#example-residue-classes-modulo-5)
    - [Structure of ( \\mathbb{Z}\_n )](#structure-of--mathbbz_n-)
  - [Properties of Congruences](#properties-of-congruences)
    - [Equivalence Properties (Reflexivity, Symmetry, Transitivity)](#equivalence-properties-reflexivity-symmetry-transitivity)
    - [Compatibility with Addition](#compatibility-with-addition)
    - [Compatibility with Multiplication](#compatibility-with-multiplication)
    - [Compatibility with Exponentiation](#compatibility-with-exponentiation)
  - [Modular Inverses](#modular-inverses)
    - [Existence and Bézout Identity](#existence-and-bézout-identity)
    - [Inverse of ( 137 \\mod 1337 )](#inverse-of--137-mod-1337-)
    - [Necessary and Sufficient Condition](#necessary-and-sufficient-condition)
  - [Bonus: Performance Analysis of Modular Exponentiation](#bonus-performance-analysis-of-modular-exponentiation)
    - [Motivation](#motivation)
    - [Naive Implementations](#naive-implementations)
    - [Timing with `timeit`](#timing-with-timeit)
    - [Benchmarking with Random Inputs](#benchmarking-with-random-inputs)
    - [Automated Comparison](#automated-comparison)
    - [Python’s `pow` Function](#pythons-pow-function)
  - [Wrap-up](#wrap-up)

# Number Theory (Part 2)

## Modular Arithmetic and Computation

Modular arithmetic is a cornerstone of modern number theory and cryptography. It enables arithmetic within a finite set of integers, and underpins protocols such as RSA, ElGamal, and Diffie–Hellman key exchange.

We begin by examining both the computational and theoretical aspects of congruences, modular operations, and inverses, ultimately building toward secure arithmetic in \( \mathbb{Z}_n \).

---

### Python’s `%` Operator

In programming languages such as Python, the symbol `%` denotes the *modulus* or *remainder* operator. For example:

```python
23 % 5  # Output: 3
```

Here, the result 3 is the remainder after dividing 23 by 5.

While useful, this operation differs slightly in conceptual motivation from that in mathematics. For a number theorist, writing:
\[
23 \equiv 3 \pmod{5}
\]
means that 23 and 3 are *congruent modulo 5*, i.e., their difference is divisible by 5:
\[
23 - 3 = 20 \equiv 0 \pmod{5}
\]

>**Congruence**: Let \( a, b \in \mathbb{Z} \), and let \( n \in \mathbb{N} \) with \( n > 0 \). We say that \( a \) is  *congruent* to \( b \) modulo \( n \), written:
>
>\[
>a \equiv b \pmod{n}
>\]
>
>if \( n \mid (a - b) \). The integer \( n \) is called the *modulus* of the congruence.

In this interpretation, we are not merely computing a remainder but entering a new arithmetic system—the set of *equivalence classes modulo 5*. The value 3 is called the **natural representative** of 23 modulo 5 within the residue class system.

---

### Reduction at Intermediate Steps

A powerful property of modular arithmetic is that reductions can be performed at every step without affecting the final result (for addition, subtraction, and multiplication). For example:

```python
((17 + 38) * (105 - 193)) % 13
```

yields the same result as:

```python
(((17 % 13) + (38 % 13)) * ((105 % 13) - (193 % 13))) % 13
```

This technique prevents unnecessary growth of numbers in computation. The effect becomes particularly significant in exponentiation.

### Example: Computing \( 3^{999} \mod 1000 \)

A naïve computation of \( 3^{999} \) produces a massive number. Instead, we reduce modulo 1000 at each step:

```python
P = 1
for _ in range(999):
    P = (P * 3) % 1000
print(P)
```

Here, all intermediate results remain below 1000, enabling efficient arithmetic even with large exponents.

---

## Residues

If \( x \equiv y \pmod{m} \), we say that \( y \) is a **residue** of \( x \) modulo \( m \).

A set \( \{x_1, x_2, \ldots, x_m\} \) is a complete residue system modulo \( m \) if for every integer \( y \in \mathbb{Z} \), there exists exactly one \( x_j \) such that:
\[
y \equiv x_j \pmod{m}.
\]

---

## Residue Classes

Modular arithmetic gives rise to a powerful and elegant structure known as *residue classes*. These are equivalence classes of integers modulo a fixed positive integer \( n \), and form the basis for defining the set of integers modulo \( n \), denoted \( \mathbb{Z}_n \).

### Congruence and Least Nonnegative Residues

For any integer \( a \), the division algorithm guarantees the existence of unique integers \( q \) and \( r \) such that:
\[
a = qn + r, \quad \text{where} \quad 0 \leq r < n.
\]
By the definition of congruence modulo \( n \), this implies:
\[
a \equiv r \pmod{n}.
\]
Hence, every integer is congruent modulo \( n \) to exactly one integer in the set:
\[
\{0, 1, 2, \ldots, n - 1\}.
\]
This set is called the **set of least nonnegative residues modulo \( n \)**.

---



### Example: Residue Classes Modulo 4

The equivalence classes modulo 4 are:

- \( \ldots \equiv -8 \equiv -4 \equiv 0 \equiv 4 \equiv 8 \equiv \ldots \pmod{4} \)
- \( \ldots \equiv -7 \equiv -3 \equiv 1 \equiv 5 \equiv 9 \equiv \ldots \pmod{4} \)
- \( \ldots \equiv -6 \equiv -2 \equiv 2 \equiv 6 \equiv 10 \equiv \ldots \pmod{4} \)
- \( \ldots \equiv -5 \equiv -1 \equiv 3 \equiv 7 \equiv 11 \equiv \ldots \pmod{4} \)

These define the residue classes:
\[
[0]_4,\ [1]_4,\ [2]_4,\ [3]_4.
\]

Thus, every integer belongs to exactly one such residue class modulo 4.

---

### Complete Residue System

A set of integers \( \{a_1, a_2, \ldots, a_n\} \) is a **complete residue system modulo \( n \)** if every integer is congruent modulo \( n \) to exactly one of the \( a_i \), and no two of the \( a_i \) are congruent to each other modulo \( n \).

In other words:
- The system contains exactly \( n \) integers.
- Each equivalence class modulo \( n \) is represented exactly once.


The integers:
\[
\{-12, -4, 11, 13, 22, 82, 91\}
\]
form a complete residue system modulo \( 7 \), because:

\[
\begin{aligned}
-12 &\equiv 2 \pmod{7}, \quad
-4  &\equiv 3 \pmod{7}, \quad
11  &\equiv 4 \pmod{7}, \\
13  &\equiv 6 \pmod{7}, \quad
22  &\equiv 1 \pmod{7}, \quad
82  &\equiv 5 \pmod{7}, \quad
91  &\equiv 0 \pmod{7}.
\end{aligned}
\]

Since each residue \( 0, 1, \ldots, 6 \) appears exactly once, the set is complete.

---



## General Structure: Residue Classes Modulo \( n \)

We now define the central object of interest.


Let \( n \in \mathbb{N}^* \). Define a relation \( \equiv_n \) on \( \mathbb{Z} \) by:
\[
a \equiv_n b \iff a \equiv b \pmod{n}.
\]

This relation \( \equiv_n \) is an **equivalence relation**, and its equivalence classes are called **residue classes modulo \( n \)**.

We denote the equivalence class of \( a \in \mathbb{Z} \) by:
\[
[a]_n = \{ x \in \mathbb{Z} : x \equiv a \pmod{n} \}.
\]

---

### Example: Residue Classes Modulo 5

\[
\begin{aligned}
[0]_5 &= \{ \ldots, -10, -5, 0, 5, 10, \ldots \} \\
[1]_5 &= \{ \ldots, -9, -4, 1, 6, 11, \ldots \} \\
[2]_5 &= \{ \ldots, -8, -3, 2, 7, 12, \ldots \} \\
[3]_5 &= \{ \ldots, -7, -2, 3, 8, 13, \ldots \} \\
[4]_5 &= \{ \ldots, -6, -1, 4, 9, 14, \ldots \}
\end{aligned}
\]

Each integer belongs to exactly one of these five residue classes.

---

### Structure of \( \mathbb{Z}_n \)

Let \( n \in \mathbb{N}^* \). Then:

- The set of residue classes modulo \( n \), denoted \( \mathbb{Z}_n \), contains exactly \( n \) elements:
\[
\mathbb{Z}_n = \{ [0]_n, [1]_n, \ldots, [n-1]_n \}.
\]
- For each \( a, b \in \mathbb{Z} \):
\[
[a]_n = [b]_n \iff a \equiv b \pmod{n}.
\]


While not the focus at this stage, it is important to note that \( \mathbb{Z}_n \), the set of residue classes modulo \( n \), possesses a rich algebraic structure. In particular:

- \( \mathbb{Z}_n \) forms a **commutative ring** with identity, where the operations of addition and multiplication are defined modulo \( n \).
- This ring structure is central to modern number theory and cryptography, and will be studied in greater detail later, particularly in the context of finite fields, group theory, and algebraic structures relevant to cryptographic protocols.

---

## Properties of Congruences

Now that we have introduced the notion of congruence and residue classes modulo \( n \), we turn to the algebraic properties that govern their behavior. These properties allow us to manipulate congruences analogously to equalities in standard arithmetic, while keeping in mind that all calculations are performed *modulo* \( n \).

### Equivalence Properties (Reflexivity, Symmetry, Transitivity)


These ensure that congruence modulo \( n \) defines an *equivalence relation* on \( \mathbb{Z} \). Let \( a, b, c, d, x, y \in \mathbb{Z} \) and \( n \in \mathbb{N} \) with \( n > 0 \). The following fundamental properties hold:

- **Reflexivity**:  
  \[
  a \equiv a \pmod{n}
  \]
- **Symmetry**:  
  \[
  a \equiv b \pmod{n} \quad \Rightarrow \quad b \equiv a \pmod{n}
  \]
- **Transitivity**:  
  \[
  a \equiv b \pmod{n} \text{ and } b \equiv c \pmod{n} \quad \Rightarrow \quad a \equiv c \pmod{n}
  \]

---

### Compatibility with Addition

Congruences are preserved under addition and additive inverses:

  \[
  a \equiv b \pmod{n} \quad \Rightarrow \quad a + c \equiv b + c \pmod{n}
  \]
  \[
  a \equiv b \pmod{n},\ c \equiv d \pmod{n} \quad \Rightarrow \quad a + c \equiv b + d \pmod{n}
  \]
  \[
  a \equiv b \pmod{n} \quad \Rightarrow \quad -a \equiv -b \pmod{n}
  \]

---

### Compatibility with Multiplication

Congruences behave predictably under multiplication:

  \[
  a \equiv b \pmod{n} \quad \Rightarrow \quad ka \equiv kb \pmod{n}, \quad \forall k \in \mathbb{Z}
  \]
  \[
  a \equiv b \pmod{n},\ c \equiv d \pmod{n} \quad \Rightarrow \quad ac \equiv bd \pmod{n}
  \]

---

### Compatibility with Exponentiation

If the base is congruent modulo \( n \), then all powers of the base remain congruent:

  \[
  a \equiv b \pmod{n} \quad \Rightarrow \quad a^k \equiv b^k \pmod{n}, \quad \forall k \in \mathbb{N}
  \]

These properties make modular arithmetic *well-behaved* under the usual operations of arithmetic, provided one is working within a fixed modulus \( n \). They are essential in proving results in number theory and cryptography, such as Fermat’s Little Theorem, Euler’s Theorem, and in the design of modular exponentiation schemes for cryptographic applications.

---

## Modular Inverses

Let \( a \in \mathbb{Z} \) and let \( n \in \mathbb{N}^* \). A **multiplicative inverse** of \( a \) modulo \( n \) is an integer \( x \in \mathbb{Z} \) such that:
\[
a \cdot x \equiv 1 \pmod{n}.
\]

Such an inverse exists if and only if \( \gcd(a, n) = 1 \), i.e., \( a \) and \( n \) are coprime. If an inverse exists, it is unique modulo \( n \), and we write:
\[
x \equiv a^{-1} \pmod{n}.
\]

> **Important**: The notation \( a^{-1} \mod n \) refers to the *modular multiplicative inverse* and must not be confused with the real-valued reciprocal \( \frac{1}{a} \), which is undefined in modular arithmetic unless the inverse exists.

---

### Existence and Bézout Identity

The existence of an inverse is guaranteed by Bézout’s identity: if \( \gcd(a, n) = 1 \), then there exist integers \( u, v \in \mathbb{Z} \) such that:
\[
au + nv = 1.
\]

Taking both sides modulo \( n \), we obtain:
\[
au \equiv 1 \pmod{n}.
\]

Hence, \( u \) is the multiplicative inverse of \( a \) modulo \( n \).

---

### Inverse of \( 137 \mod 1337 \)

We want to compute:
\[
137^{-1} \mod 1337.
\]

Using the extended Euclidean algorithm, we find:
\[
1 = 1337 \cdot (-54) + 137 \cdot 527.
\]

Taking both sides modulo 1337, we obtain:
\[
137 \cdot 527 \equiv 1 \pmod{1337}.
\]

Thus, the modular inverse is:
\[
\boxed{137^{-1} \equiv 527 \mod 1337}.
\]


Modular inverses can be computed efficiently using the **Extended Euclidean Algorithm** or built-in functions in computational systems.

In Python (via `Crypto.Util.number`):
```python
from Crypto.Util.number import inverse
inverse(137, 1337)  # Output: 527
```

In SageMath:
```sage
pow(137, -1, 1337)
# Output: 527
```

Both approaches are based on the underlying implementation of the extended Euclidean algorithm.

---

### Necessary and Sufficient Condition

Let \( a, n \in \mathbb{Z} \). Then:

- \( a \) is invertible modulo \( n \) if and only if:
\[
\gcd(a, n) = 1.
\]

This criterion is central in number theory and cryptography. For instance, in RSA, decryption relies on computing the inverse of the encryption exponent modulo \( \varphi(n) \).

The concept of a modular inverse is foundational in modular arithmetic and appears throughout cryptographic protocols. Whether determining decryption keys or computing signatures, the ability to efficiently compute and reason about inverses modulo \( n \) is critical. The Extended Euclidean Algorithm not only proves the existence of such inverses when they exist, but also enables practical computation in both symbolic and applied contexts.


---

## Bonus: Performance Analysis of Modular Exponentiation

### Motivation

Efficient computation of modular exponentiation is fundamental in cryptography. Many cryptographic algorithms, such as RSA, rely heavily on evaluating expressions of the form:

\[
a^k \mod m
\]

While modular arithmetic theoretically ensures that intermediate results can be reduced modulo \( m \) at each step, performance varies significantly depending on implementation. We explore this with a comparative performance analysis of several methods.

---

### Naive Implementations

We define two basic approaches to compute \( a^k \mod m \).

```python
def powermod_1(base, exponent, modulus):
    return (base**exponent) % modulus  # Naive: exponentiate first, then reduce

def powermod_2(base, exponent, modulus):
    P = 1
    for _ in range(exponent):
        P = (P * base) % modulus  # Iterative reduction
    return P
```

Although `powermod_2` applies modular reduction at each multiplication step—thus avoiding large intermediate values—it is not always faster.

---

### Timing with `timeit`


```python
import timeit as TI
print(TI.timeit('powermod_1(3, 999, 1000)', "from __main__ import powermod_1", number=10000))
print(TI.timeit('powermod_2(3, 999, 1000)', "from __main__ import powermod_2", number=10000))
```

The `number` argument specifies the number of repetitions. The result is the total elapsed time, so average time per run can be obtained by dividing by this number.

---

### Benchmarking with Random Inputs

We can assess expected runtime across randomized input values. Using Python’s `random.randint`, we simulate a broad input space:

```python
from random import randint

Freq = {i: 0 for i in range(1, 11)}
for _ in range(10000):
    Freq[randint(1, 10)] += 1
```

For visualization:

```python
import matplotlib.pyplot as plt
plt.bar(Freq.keys(), Freq.values())
plt.show()
```

---

### Automated Comparison

We now compare both methods over 1000 random samples:

```python
time_1 = 0
time_2 = 0

for _ in range(1000):
    base = randint(10, 99)
    exponent = randint(1000, 1999)
    modulus = randint(1000, 1999)

    time_1 += TI.timeit('powermod_1(base, exponent, modulus)', 
                        "from __main__ import powermod_1, base, exponent, modulus", number=10)

    time_2 += TI.timeit('powermod_2(base, exponent, modulus)', 
                        "from __main__ import powermod_2, base, exponent, modulus", number=10)

print("powermod_1 total time: {:.5f} seconds".format(time_1))
print("powermod_2 total time: {:.5f} seconds".format(time_2))
```

Typically, `powermod_1` is faster due to Python's highly optimized internal `**` operator.

---

We explored why `powermod_1` outperforms `powermod_2`:

- The modular reduction `%` is extremely fast (nanoseconds).
- Built-in operators like `**` are implemented in C and compiled to machine code.
- Our loop in `powermod_2` uses more multiplications than necessary.

```python
print(TI.timeit('1238712 % 1237')) # Extremely fast
```

---

### Python’s `pow` Function

Python provides a specialized three-argument `pow(base, exponent, modulus)` function that performs modular exponentiation efficiently:

```python
pow(3, 999)             # Returns a large integer
pow(3, 999, 1000)       # Efficiently computes (3^999) % 1000
pow(3, 999) % 1000      # Less efficient than built-in pow with three arguments

print(TI.timeit('pow(3, 999, 1000)'))
print(TI.timeit('pow(3, 999) % 1000'))
```

The three-argument version is significantly faster due to internal optimizations using *modular exponentiation algorithms* such as **exponentiation by squaring**.


The performance analysis above illustrates a broader principle in algorithm design:

> *Built-in operations, implemented in low-level languages and optimized for speed, are generally faster than user-defined loops in high-level languages like Python.*

However, understanding the algorithm behind modular exponentiation remains essential. It allows us to:

- Write portable and language-agnostic implementations.
- Modify algorithms when cryptographic needs arise.
- Analyze complexity and security in cryptographic primitives.

## Wrap-up 

In this part, we explored the foundations of *modular arithmetic*, a central theme in number theory and cryptography. We introduced the concept of congruence modulo \( n \), examined the structure of the residue classes \( \mathbb{Z}_n \), and studied how arithmetic operations—addition, subtraction, multiplication, and exponentiation—behave under congruence relations.

We also clarified the distinction between the computational `%` operator in programming and the formal equivalence \( a \equiv b \pmod{n} \) in mathematics, emphasizing their interconnected roles.

Most importantly, we established that modular arithmetic respects the familiar rules of arithmetic, allowing us to reduce intermediate results *modulo* \( n \) at every step without affecting the final outcome. This property is not only elegant but also highly efficient in practical computations, especially in cryptographic protocols where large integers are involved.
