- [Number Theory (Part I)](#number-theory-part-i)
  - [The Integers ( \\mathbb{Z} )](#the-integers--mathbbz-)
    - [Properties](#properties)
  - [Divisibility and Division](#divisibility-and-division)
    - [Elementary Properties of Divisibility](#elementary-properties-of-divisibility)
    - [Divisibility Rules](#divisibility-rules)
  - [Division with Remainder](#division-with-remainder)
    - [Alternate Formulas](#alternate-formulas)
  - [Divisibility, GCD, LCM, and the Euclidean Algorithm](#divisibility-gcd-lcm-and-the-euclidean-algorithm)
    - [Divisibility and Common Divisors](#divisibility-and-common-divisors)
    - [Basic Properties of Divisibility](#basic-properties-of-divisibility)
    - [Greatest Common Divisor (GCD)](#greatest-common-divisor-gcd)
    - [Least Common Multiple (LCM)](#least-common-multiple-lcm)
    - [Euclidean Algorithm](#euclidean-algorithm)
    - [Python Implementations](#python-implementations)
  - [Extended Euclidean Algorithm](#extended-euclidean-algorithm)

# Number Theory (Part I)

In this part, we establish foundational concepts in number theory, which are essential for understanding the mathematical underpinnings of modern cryptographic protocols. These ideas form the basis for techniques used in public-key encryption, digital signatures, secure communication, and more.

Our primary computational tools will be SageMath and Python, which offer both theoretical depth and practical efficiency for symbolic and numeric computations.

We begin by studying the arithmetic of integers—focusing on notions such as divisibility, common divisors, and the Euclidean algorithm—which naturally lead to more advanced concepts like modular arithmetic, multiplicative inverses, and congruences. These topics are not only fundamental in abstract number theory but are also indispensable for cryptographic systems such as RSA, Diffie–Hellman, and elliptic curve cryptography.

---

## The Integers \( \mathbb{Z} \)

The set of integers is defined as:
\[
\mathbb{Z} = \{ \ldots, -3, -2, -1, 0, 1, 2, 3, \ldots \}
\]
This set extends the natural numbers to include zero and the additive inverses of positive integers.

### Properties

- *Closure*: The set \( \mathbb{Z} \) is closed under addition, subtraction, and multiplication. That is, if \( a, b \in \mathbb{Z} \), then \( a + b, a - b, ab \in \mathbb{Z} \).

- *Subtraction via additive inverse*:
  \[
  a - b := a + (-b)
  \]
  where \( -b \) is the additive inverse of \( b \in \mathbb{Z} \). This formulation guarantees subtraction is always defined.

---

## Divisibility and Division

A fundamental question in number theory is whether one integer can be *evenly divided* by another.

>Let \( a, b \in \mathbb{Z} \) with \( b \ne 0 \). We say that \( b \) *divides* \( a \), written \( b \mid a \), if there exists an integer \( k \) such that:
\[
a = bk
\]

In this case, \( a \) is a *multiple* of \( b \), and \( b \) is a *divisor* or *factor* of \( a \).

### Elementary Properties of Divisibility

Let \( a, b, c \in \mathbb{Z} \). Then:

1. \( a \mid a \)
2. If \( a \mid b \) and \( b \mid c \), then \( a \mid c \)
3. If \( a \mid b \) and \( a \mid c \), then \( a \mid (bx + cy) \) for all \( x, y \in \mathbb{Z} \)
4. If \( a \mid b \) and \( b \mid a \), then \( a = \pm b \)

### Divisibility Rules

Divisibility rules offer quick checks for common divisors.

> Example Rule for 2 : 
>
>An integer is divisible by 2 *if and only if* its last digit is:
>\[
>0,\, 2,\, 4,\, 6,\, 8
>\]
>
>These digits define the class of *even numbers*.

Rules for divisibility by other integers (3, 5, 9, 11, etc.) will be addressed in a later section.

---

## Division with Remainder

Given integers \( a \in \mathbb{Z} \) and \( b \in \mathbb{Z} \) with \( b > 0 \), the **division algorithm** guarantees the existence of unique integers \( q \) and \( r \) such that:

\[
a = bq + r, \quad 0 \leq r < b
\]

- \( q \) is called the *quotient*.
- \( r \) is called the *remainder*.

This pair \( (q, r) \) is *uniquely determined* by the values of \( a \) and \( b \).

The remainder \( r \) is often denoted:
\[
a \pmod b
\]
and the quotient \( q \) is denoted:
\[
a \div b
\]

### Alternate Formulas

For any \( a, b \in \mathbb{Z} \) with \( b \ne 0 \), we may also write:

\[
a \div b = \left\lfloor \frac{a}{b} \right\rfloor, \quad a \pmod b = a - b \left\lfloor \frac{a}{b} \right\rfloor
\]

These definitions align with computational implementations.

```python
print(15 % 5)  # Output: 0
```

This confirms that 15 is divisible by 5, as the remainder is zero.

---

## Divisibility, GCD, LCM, and the Euclidean Algorithm

### Divisibility and Common Divisors

Let \( a, b \in \mathbb{Z} \). We say that:

- \( a \mid b \) (read as “\( a \) divides \( b \)”) if there exists an integer \( k \in \mathbb{Z} \) such that:
  \[
  b = a \cdot k
  \]

A number \( c \in \mathbb{Z} \) is called a *common divisor* of \( a \) and \( b \) if \( c \mid a \) and \( c \mid b \).

### Basic Properties of Divisibility

For all \( a, b, c \in \mathbb{Z} \):

- \( a \mid a \)
- If \( a \mid b \) and \( b \mid c \), then \( a \mid c \)
- If \( a \mid b \) and \( a \mid c \), then for all \( x, y \in \mathbb{Z} \), we have \( a \mid (bx + cy) \)
- If \( a \mid b \) and \( b \mid a \), then \( a = \pm b \)

---

### Greatest Common Divisor (GCD)

The *greatest common divisor* of two integers \( a \) and \( b \), denoted \( \gcd(a, b) \), is the largest positive integer \( d \) satisfying:

1. \( d \mid a \) and \( d \mid b \)
2. If \( c \mid a \) and \( c \mid b \), then \( c \mid d \)

By convention:
\[
\gcd(0, 0) = 0
\]

---

### Least Common Multiple (LCM)

The *least common multiple* of \( a \) and \( b \), denoted \( \mathrm{lcm}(a, b) \), is the smallest positive integer \( d \) such that:

1. \( a \mid d \) and \( b \mid d \)
2. If \( a \mid c \) and \( b \mid c \), then \( d \mid c \)

By convention:
\[
\mathrm{lcm}(0, 0) = 0
\]

For \( a, b > 0 \), there is a fundamental identity:
\[
\mathrm{lcm}(a, b) = \frac{a \cdot b}{\gcd(a, b)}
\]

---

### Euclidean Algorithm

To compute \( \gcd(a, b) \), one uses the recursive identity:
\[
\gcd(a, b) = \gcd(b, a \bmod b)
\]

This is valid since the set of common divisors of \( a \) and \( b \) is equal to the set of common divisors of \( b \) and \( r = a \bmod b \).

As an example, we calculated the following \( \gcd(1337, 137) \):

\[
\begin{aligned}
1337 &= 137 \cdot 9 + 104 \\
137 &= 104 \cdot 1 + 33 \\
104 &= 33 \cdot 3 + 5 \\
33  &= 5 \cdot 6 + 3 \\
5   &= 3 \cdot 1 + 2 \\
3   &= 2 \cdot 1 + 1 \\
2   &= 1 \cdot 2 + 0
\end{aligned}
\]

Thus:
\[
\gcd(1337, 137) = 1
\]

---

### Python Implementations

We have a *Recursive Version*:

```python
def our_gcd(a, b):
    if b == 0:
        return a
    return our_gcd(b, a % b)
```

We also have an *Iterative Version*:

```python
def GCD(a, b):
    while b:
        a, b = b, a % b
    return abs(a)
```

And lastly a *Verbose Version* (with print statements): 

```python
def Euclidean_algorithm(a, b):
    while b:
        q = a // b
        r = a % b
        print(f"{a} = {q}({b}) + {r}")
        a, b = b, r
```

Stay a bit, and think which are the differences between these versions...

---

## Extended Euclidean Algorithm

The *Extended Euclidean Algorithm* computes not only \( \gcd(a, b) \), but also integers \( x, y \in \mathbb{Z} \) such that:

\[
\gcd(a, b) = ax + by
\]

These integers \( x, y \) are the *Bézout coefficients*, and the identity is known as the *Bézout identity*.

```python
def our_xgcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = our_xgcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1
```

We proceed with a simple example:

>Find the  \( \gcd(1337, 137) \)

Rewriting the previous Euclidean steps backward, we get:

\[
1 = 1337 \cdot (-54) + 137 \cdot 527
\]

Thus:
\[
x = -54,\quad y = 527
\]

Certainly — here is a formal and academic adaptation of your insight, ready to integrate smoothly into your text:

---

Despite the extensive development of the theory — from recursive identities and Bézout's coefficients to multiple algorithmic implementations — in practice, these computations often reduce to a single line of code using pre-built functions.

For instance, in **SageMath**, one can simply write:

```sage
gcd(a, b)           # Computes the greatest common divisor
xgcd(a, b)          # Returns (gcd, x, y) satisfying Bézout's identity: gcd = ax + by
```

Likewise, in **Python**, using either standard or cryptographic libraries:

```python
from math import gcd
gcd(a, b)
```

or:

```python
from Crypto.Util.number import GCD, inverse
GCD(a, b)
```

This illustrates a broader phenomenon common in both mathematics and computer science: one first learns to construct a tool from fundamental principles — in this case, the Euclidean algorithm and its extended form — only to later rely on highly optimized, abstracted library implementations.

However, understanding the underlying theory remains indispensable. It is precisely this knowledge that allows one to apply such tools correctly, assess their limitations, adapt them in cryptographic settings, and reason rigorously about their behavior and correctness.

---

And with that, we conclude our journey through *divisibility* and the *Euclidean algorithm*. These foundational ideas — simple in form, yet powerful in consequence — prepare us for deeper investigations into the world of modular arithmetic.

Up next: we explore *modular inverses*, *congruences*, and other essential tools that underpin modern cryptography. Buckle up — the mathematical adventure is just beginning.









