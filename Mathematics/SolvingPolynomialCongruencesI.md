- [Solving Polynomial Congruences (Part I)](#solving-polynomial-congruences-part-i)
  - [Introduction and Linear Congruences](#introduction-and-linear-congruences)
    - [Special Case: When ( a ) Is a Unit Modulo ( m )](#special-case-when--a--is-a-unit-modulo--m-)
  - [Linear Diophantine Equations and Modular Inverses](#linear-diophantine-equations-and-modular-inverses)
    - [The Extended Euclidean Algorithm](#the-extended-euclidean-algorithm)
    - [Application to Modular Inverses](#application-to-modular-inverses)
  - [Hop-and-Skip: Tracking the Linear Combination](#hop-and-skip-tracking-the-linear-combination)
  - [Congruences of Higher Degree](#congruences-of-higher-degree)
  - [Lifting Solutions Modulo ( p ) to ( p^\\alpha )](#lifting-solutions-modulo--p--to--palpha-)
    - [Number of Solutions](#number-of-solutions)
    - [Hensel's Lemma](#hensels-lemma)
  - [Some Computational Validation](#some-computational-validation)
  - [Wrap-up](#wrap-up)


# Solving Polynomial Congruences (Part I)

Having laid the foundation of *modular arithmetic* and *congruences*, we are now ready to advance into one of the richest areas of number theory: *solving polynomial congruences*.

In this part, we will explore a wide range of topics that build upon modular thinking. We begin with the study of *linear congruences*, closely connected to *linear Diophantine equations* — equations that seek integer solutions to expressions like \( ax + by = c \). Understanding these will give us the necessary tools to solve basic modular equations.

As we move to polynomials of higher degree, we will encounter fascinating classical problems, such as:

- **Pythagorean triples** — the integer solutions to \( x^2 + y^2 = z^2 \), studied since the time of Pythagoras.
- **Fermat's Last Theorem** — a far-reaching generalization, asserting that the equation \( x^n + y^n = z^n \) has no nontrivial integer solutions for \( n \geq 3 \), a statement that connects deeply with **modular forms** and **elliptic curves**.
- **Pell’s equations** — another classical topic, centered on solving \( x^2 - dy^2 = 1 \) in integers, with deep applications to algebraic number theory and cryptographic constructions.

Along the way, we will discover the profound connections among these topics, and how tools like modular arithmetic, Diophantine methods, and polynomial techniques interact to solve some of the most important problems in mathematics — many of which underpin modern cryptography.

It becomes clear that *Diophantus*, the ancient mathematician after whom "Diophantine equations" are named, laid the groundwork for much of what we explore even today in advanced mathematics and cryptographic protocols.

> **In short:** this topic will be a rich journey from the classical worlds of Pythagoras and Fermat to the modern realms of cryptographic security — all starting with the humble task of solving congruences.

So, buckle up — and let us begin!

---

## Introduction and Linear Congruences

We are particularly interested in congruences of the form:

\[
f(x) \equiv 0 \pmod{m},
\]

where \( f(x) = a_nx^n + \dots + a_1x + a_0 \) is a polynomial with integer coefficients, and \( m > 0 \).

Since modular congruence preserves polynomial evaluation — that is, \( a \equiv b \pmod{m} \implies f(a) \equiv f(b) \pmod{m} \) — solving such congruences amounts to finding appropriate residue classes in \( \mathbb{Z}/m\mathbb{Z} \).  
Thus, the set of solutions is *finite*, corresponding to a subset of \( \mathbb{Z}_m \).


We begin with the simplest case: solving *linear congruences* of the form:

\[
ax \equiv b \pmod{m}.
\]

A fundamental theorem governs their solvability:

> **Theorem (Solvability of Linear Congruences):**  
> Let \( a, b, m \in \mathbb{Z} \) with \( m > 0 \). Then:
> - The congruence \( ax \equiv b \pmod{m} \) has a solution if and only if \( \gcd(a, m) \mid b \).
> - If a solution exists, there are exactly \( \gcd(a, m) \) incongruent solutions modulo \( m \).

In particular, when \( \gcd(a, m) = 1 \), there exists exactly **one** solution modulo \( m \).


**Remark:** Solving linear congruences is closely related to solving *linear Diophantine equations* of the form:

\[
ax - my = b,
\]

for integers \( x \) and \( y \).  
We will explore this connection in full detail later.

---

### Special Case: When \( a \) Is a Unit Modulo \( m \)

If \( a \in \mathbb{Z}_m^* \) — that is, \( \gcd(a, m) = 1 \) — then \( a \) possesses a **multiplicative inverse** modulo \( m \), denoted \( a^{-1} \).

In this case, the congruence:

\[
ax \equiv b \pmod{m}
\]
has the unique solution:

\[
x \equiv a^{-1}b \pmod{m}.
\]

Finding modular inverses is a fundamental task. According to **Euler’s theorem**:

\[
x^{\varphi(m)} \equiv 1 \pmod{m},
\]
where \( \varphi(m) \) is Euler’s totient function, counting the units of \( \mathbb{Z}_m \).  
Thus:

\[
x^{-1} \equiv x^{\varphi(m) - 1} \pmod{m}.
\]

*Example*: Consider the congruence:

\[
34x \equiv 60 \pmod{98}.
\]

First, observe:

\[
\gcd(34, 98) = 2,
\]
and since \( 2 \mid 60 \), solutions exist.

We divide through by 2:

\[
17x \equiv 30 \pmod{49}.
\]

To solve this, one approach is to find the modular inverse of 17 modulo 49 using the extended Euclidean algorithm (discussed later).  
Alternatively, solving the associated linear Diophantine equation:

\[
17x - 49y = 30
\]
provides a solution.

Proceeding by standard techniques, we find a particular solution \( x \equiv -4 \pmod{49} \).

Thus, the two solutions to the original congruence modulo 98 are:

\[
x \equiv -4 \pmod{49} \quad \text{and} \quad x \equiv 45 \pmod{98}.
\]

---

## Linear Diophantine Equations and Modular Inverses

Having observed the connection between linear congruences and Diophantine equations, we now formally develop the theory of the diophantine equations.

A **linear Diophantine equation** is any equation of the form:

\[
ax + by = c,
\]
where \( a, b, c \in \mathbb{Z} \), and the goal is to find integer solutions \( (x, y) \).


The equation \( ax + by = c \) has integer solutions if and only if:

\[
\gcd(a, b) \mid c.
\]

If \( g = \gcd(a, b) \), and \( g \mid c \), then multiplying a Bézout identity for \( (a, b) \) by \( \frac{c}{g} \) provides a particular solution.

All solutions are given parametrically by:

\[
x = x_0 + \frac{b}{g}n, \quad
y = y_0 - \frac{a}{g}n, \quad n \in \mathbb{Z},
\]
where \( (x_0, y_0) \) is a particular solution.


### The Extended Euclidean Algorithm

The **Extended Euclidean Algorithm** provides an efficient method to compute not only the gcd of two integers, but also integers \( x, y \) satisfying:

\[
ax + by = \gcd(a, b).
\]

This expression is known as a **Bézout identity**.

### Application to Modular Inverses

When \( \gcd(a, n) = 1 \), solving:

\[
ax \equiv 1 \pmod{n}
\]
is equivalent to finding integers \( x, y \) such that:

\[
ax + ny = 1.
\]

Thus, \( x \) modulo \( n \) gives the modular inverse:

\[
x \equiv a^{-1} \pmod{n}.
\]


Let us compute the inverse of \( 130 \) modulo \( 61 \).

Applying the Euclidean algorithm:

\[
\begin{aligned}
130 &= 2 \times 61 + 8, \\
61 &= 7 \times 8 + 5, \\
8 &= 1 \times 5 + 3, \\
5 &= 1 \times 3 + 2, \\
3 &= 1 \times 2 + 1, \\
2 &= 2 \times 1 + 0.
\end{aligned}
\]

Working backwards:

\[
1 = 3 - 1 \times 2,
\quad 2 = 5 - 1 \times 3,
\quad 3 = 8 - 1 \times 5,
\quad 5 = 61 - 7 \times 8,
\quad 8 = 130 - 2 \times 61,
\]

substituting step by step yields:

\[
1 = 23 \times 130 - 49 \times 61.
\]

Thus:

\[
130^{-1} \equiv 23 \pmod{61}.
\]

--- 

## Hop-and-Skip: Tracking the Linear Combination

The algorithm below mimics the steps of the Euclidean algorithm while *keeping track* of how each remainder is built from the original \( a \) and \( b \). It uses "hops" (multiples of \( a \)) and "skips" (multiples of \( b \)).

```python
def hop_and_skip(a, b):
    """
    Computes the Bézout identity: gcd(a, b) = x * a + y * b
    using a traceable version of the Euclidean algorithm.
    """
    u, v = a, b
    u_hops, u_skips = 1, 0
    v_hops, v_skips = 0, 1

    while v != 0:
        q = u // v
        r = u % v
        r_hops = u_hops - q * v_hops
        r_skips = u_skips - q * v_skips

        u, v = v, r
        u_hops, v_hops = v_hops, r_hops
        u_skips, v_skips = v_skips, r_skips

    print(f"{u} = {u_hops}*{a} + {u_skips}*{b}")
```

We now assemble a solver for the linear Diophantine equation \( ax + by = c \). This function determines whether solutions exist, and if so, prints all solutions in parametric form.

```python
def solve_LDE(a, b, c):
    """
    Solves the equation ax + by = c for integer x, y.
    Returns one solution (x, y) if it exists, otherwise None.
    """
    u, v = a, b
    u_hops, u_skips = 1, 0
    v_hops, v_skips = 0, 1

    while v != 0:
        q = u // v
        r = u % v
        r_hops = u_hops - q * v_hops
        r_skips = u_skips - q * v_skips

        u, v = v, r
        u_hops, v_hops = v_hops, r_hops
        u_skips, v_skips = v_skips, r_skips

    g = u  # gcd(a, b)

    if c % g == 0:
        d = c // g
        x = d * u_hops
        y = d * u_skips
        print(f"{a}x + {b}y = {c} has solutions if and only if:")
        print(f"x = {x} + {b // g}n, y = {y} - {a // g}n for n in ℤ.")
        return x, y
    else:
        print(f"No solutions exist for {a}x + {b}y = {c} because gcd({a}, {b}) = {g} does not divide {c}.")
    return None

```
We want to solve the following equation: 

\[
1337x + 137y = 1
\]

```python
print(solve_LDE(1337, 137, 1))
```

Output:

```
1337x + 137y = 1 has solutions if and only if:
x = -54 + 137n, y = 527 - 1337n for n in ℤ.
```

---

## Congruences of Higher Degree

We now return on the general case that we pointed out in the beginning so we consider polynomial congruences of the form:
\[
f(x) = a_0x^n + a_1x^{n-1} + \cdots + a_n \equiv 0 \pmod{m},
\]
where not all coefficients \( a_i \in \mathbb{Z} \) are divisible by \( m \). This is a natural extension of our previous study on linear congruences.

Let the modulus \( m \) have prime-power decomposition:
\[
m = \prod_{i=1}^r p_i^{\alpha_i}.
\]
Then, by the *Chinese Remainder Theorem*, solving \( f(x) \equiv 0 \pmod{m} \) is equivalent to solving the system of congruences:
\[
f(x) \equiv 0 \pmod{p_1^{\alpha_1}}, \quad \ldots, \quad f(x) \equiv 0 \pmod{p_r^{\alpha_r}}.
\]

If for each \( i \), the congruence \( f(x) \equiv 0 \pmod{p_i^{\alpha_i}} \) has a root \( c_i \), then the system:
\[
x \equiv c_1 \pmod{p_1^{\alpha_1}}, \quad \ldots, \quad x \equiv c_r \pmod{p_r^{\alpha_r}}
\]
has a unique solution modulo \( m \), and this solution is also a solution of the original congruence. Thus, the number of solutions modulo \( m \) is equal to the *product of the number of solutions modulo each \( p_i^{\alpha_i} \)*.

Hence, we are reduced to the study of congruences modulo powers of primes. And even more: using *lifting techniques*, we can reduce these to congruences modulo \( p \), where \( p \) is prime.

---

## Lifting Solutions Modulo \( p \) to \( p^\alpha \)

Suppose we are interested in solving the congruence:

\[
f(x) \equiv 0 \pmod{p^\alpha},
\]
where \( p \) is a prime number and \( \alpha \geq 1 \), and we already know a solution \( a \) modulo \( p^\beta \) for some \( \beta < \alpha \), that is:

\[
f(a) \equiv 0 \pmod{p^\beta}.
\]

We seek to *lift* this solution to a solution modulo \( p^{\beta+1} \).

Let us set:

\[
x = a + tp^\beta,
\]
where \( t \in \mathbb{Z} \) is to be determined. Expanding \( f(x) \) around \( a \) using *Taylor's formula*, we obtain:

\[
f(a + tp^\beta) = f(a) + tp^\beta f'(a) + \frac{(tp^\beta)^2}{2!} f''(a) + \cdots + \frac{(tp^\beta)^n}{n!} f^{(n)}(a).
\]

Working modulo \( p^{\beta+1} \), observe that:

- Each term involving \( (tp^\beta)^k \) for \( k \geq 2 \) is divisible by \( p^{2\beta} \),
- Since \( 2\beta \geq \beta + 1 \) when \( \beta \geq 1 \), these higher-order terms vanish modulo \( p^{\beta+1} \).

Thus, modulo \( p^{\beta+1} \), the expansion simplifies to:

\[
f(a + tp^\beta) \equiv f(a) + tp^\beta f'(a) \pmod{p^{\beta+1}}.
\]

Since \( f(a) \equiv 0 \pmod{p^\beta} \), we can express:

\[
f(a) = p^\beta k
\]
for some \( k \in \mathbb{Z} \).

Substituting into the simplified expansion, the lifting condition becomes:

\[
f(a + tp^\beta) \equiv p^\beta (k + tf'(a)) \equiv 0 \pmod{p^{\beta+1}}.
\]

Dividing both sides by \( p^\beta \) (which is allowed modulo \( p^{\beta+1} \)) leads to the congruence:

\[
k + t f'(a) \equiv 0 \pmod{p},
\]
or equivalently:

\[
f'(a) t \equiv -\frac{f(a)}{p^\beta} \pmod{p}.
\]

Thus, *lifting the solution* reduces to solving a *linear congruence modulo \( p \)*.


### Number of Solutions

The number of solutions to the congruence:

\[
f'(a) t \equiv -\frac{f(a)}{p^\beta} \pmod{p}
\]
depends on the divisibility properties of \( f'(a) \) and \( \frac{f(a)}{p^\beta} \) modulo \( p \):

\[
\# \text{Solutions} =
\begin{cases}
0, & \text{if } p \mid f'(a) \text{ and } p \nmid \frac{f(a)}{p^\beta}, \\[6pt]
p, & \text{if } p \mid f'(a) \text{ and } p \mid \frac{f(a)}{p^\beta}, \\[6pt]
1, & \text{if } p \nmid f'(a).
\end{cases}
\]


### Hensel's Lemma

This lifting principle leads to a fundamental result known as *Hensel’s lemma*:

>Let \( p \) be a prime number, \( k \geq 1 \), and let \( f(x) \in \mathbb{Z}[x] \) be a polynomial with integer coefficients.
>
>Suppose \( a \in \mathbb{Z} \) satisfies:
>
>\[
>f(a) \equiv 0 \pmod{p^k}.
>\]
>
>Then:
>
>- If \( f'(a) \not\equiv 0 \pmod{p} \), there exists a *unique* \( \tilde{a} \in \mathbb{Z} \) such that:
>
>\[
>\tilde{a} \equiv a \pmod{p^k}
>\quad \text{and} \quad
>f(\tilde{a}) \equiv 0 \pmod{p^{k+1}}.
>\]
>
>- If \( f'(a) \equiv 0 \pmod{p} \) and \( f(a) \equiv 0 \pmod{p^{k+1}} \), then there are *exactly \( p \)* solutions modulo \( p^{k+1} \) lifting \( a \).
>- If \( f'(a) \equiv 0 \pmod{p} \) and \( f(a) \not\equiv 0 \pmod{p^{k+1}} \), then *no* lifting exists.

Thus, Hensel’s lemma provides a powerful method to iteratively lift solutions from \( \pmod{p} \) to \( \pmod{p^k} \) for arbitrary \( k \geq 1 \).


Below we provide two examples, the first one is a simple one and the latter is a harder one involving also CRT.

*Example 1*: Solve \( f(x) = x^3 - 4x^2 + 5x - 6 \equiv 0 \pmod{27} \)

Let’s follow the lifting method step-by-step.

- **Step 1: Solve modulo \( p = 3 \)**

We reduce:
\[
f(x) = x^3 - 4x^2 + 5x - 6 \equiv x^3 + 2x^2 + 2x \pmod{3}
\]
Check \( x = 0, 1, 2 \):
- \( x = 0 \Rightarrow 0 \)
- \( x = 1 \Rightarrow 1 + 2 + 2 = 5 \not\equiv 0 \)
- \( x = 2 \Rightarrow 8 + 8 + 4 = 20 \not\equiv 0 \)

Only solution is \( x \equiv 0 \pmod{3} \).

- **Step 2: Lift to modulo \( 9 \)**

Let \( x = 0 + 3t \), and we want:
\[
f(3t) \equiv 0 \pmod{9}
\]
Use:
\[
f(a + 3t) \equiv f(a) + 3t f'(a) \pmod{9}, \quad \text{where } a = 0
\]
\[
f(0) = -6,\quad f'(x) = 3x^2 - 8x + 5,\quad f'(0) = 5
\]

So:
\[
3 \cdot 5 \cdot t \equiv 6 \pmod{9} \Rightarrow 15t \equiv 6 \pmod{9} \Rightarrow 5t \equiv 2 \pmod{3}
\Rightarrow t \equiv 1 \pmod{3}.
\]
Let \( t = 1 + 3t_1 \), so \( x = 3 + 9t_1 \).

- **Step 3: Lift to modulo \( 27 \)**

Now \( x = 3 + 9t_1 \). Compute:
\[
f(x) \equiv f(3) + 9t_1 f'(3) \pmod{27}
\]
\[
f(3) = 27 - 36 + 15 - 6 = 0, \quad f'(3) = 3 \cdot 9 - 24 + 5 = 8
\]
\[
f(x) \equiv 0 + 9t_1 \cdot 8 = 72t_1 \pmod{27} \Rightarrow t_1 \equiv 0 \pmod{3}
\]
Let \( t_1 = 3t_2 \), so \( x = 3 + 27t_2 \Rightarrow x \equiv 3 \pmod{27} \)

Our final solution:
\[
\boxed{x \equiv 3 \pmod{27}}
\]


So to summarize a bit of the idea behind the lifting method here are some tips: 

1. Solve the congruence \( f(x) \equiv 0 \pmod{p} \).
2. For each solution \( a_1 \), attempt to lift to a solution modulo \( p^2 \), \( p^3 \), ..., up to \( p^\alpha \).
3. At each step, use:
   \[
   f'(a_k)t \equiv -\frac{f(a_k)}{p^k} \pmod{p}
   \]
4. Repeat recursively, exploring all solution branches.

This recursive lifting technique lies at the heart of *Hensel’s Lemma* and will be indispensable in our upcoming study of elliptic curves and modular forms in cryptography.

---
We proceed now with an example that is a combination of Hensel’s Lemma and the CRT:

*Example 2*: We wish to solve the congruence:

\[
x^2 + 3x + 17 \equiv 0 \pmod{315}.
\]


- **Step 1: Factor the Modulus**

First, observe that:

\[
315 = 3^2 \times 5 \times 7.
\]

Thus, we can *decompose* the original problem into solving separately modulo \( 9 \), \( 5 \), and \( 7 \), and then combining solutions using the CRT.

That is, solve the system:

\[
\begin{aligned}
x^2 + 3x + 17 &\equiv 0 \pmod{9}, \quad \text{(A)}\\
x^2 + 3x + 17 &\equiv 0 \pmod{5}, \quad \text{(B)}\\
x^2 + 3x + 17 &\equiv 0 \pmod{7}. \quad \text{(C)}
\end{aligned}
\]

- **Step 2: Solve Modulo \( 9 \) — Using Hensel’s Lemma**

We first tackle congruence (A).

Since \( 9 = 3^2 \), we first solve modulo \( 3 \), and then *lift* solutions modulo \( 9 \) using *Hensel’s lemma**.

First, solve for modulo 3:

\[
x^2 + 3x + 17 \equiv x^2 + 0x + 2 \equiv x^2 + 2 \equiv 0 \pmod{3}.
\]

Thus:

\[
x^2 \equiv 1 \pmod{3}.
\]

Testing by trial:

- \( x \equiv 1 \pmod{3} \): \( 1^2 = 1 \equiv 1 \pmod{3} \) ✅
- \( x \equiv 2 \pmod{3} \): \( 2^2 = 4 \equiv 1 \pmod{3} \) ✅

Thus, \( x \equiv 1 \) and \( x \equiv 2 \mod 3 \) are solutions.

Now, apply *Hensel’s lemma* to lift each solution from modulo \( 3 \) to modulo \( 9 \).

Let’s first consider \( x \equiv 1 \mod 3 \).

Set \( x = 1 + 3t \) and plug into \( f(x) \mod 9 \):

\[
f(1 + 3t) \equiv 0 \pmod{9}.
\]

Expand:

\[
(1 + 3t)^2 + 3(1 + 3t) + 17 = (1 + 6t + 9t^2) + (3 + 9t) + 17,
\]
\[
= 21 + 15t + 9t^2.
\]

Modulo 9:

\[
21 + 15t + 9t^2 \equiv 3 + 6t \pmod{9}.
\]

Thus, the lifting condition is:

\[
3 + 6t \equiv 0 \pmod{9}.
\]
\[
6t \equiv -3 \equiv 6 \pmod{9}.
\]
\[
t \equiv 1 \pmod{3}.
\]

Thus, \( t = 1 \) modulo 3, so:

\[
x = 1 + 3 \times 1 = 4 \pmod{9}.
\]

Similarly, for \( x \equiv 2 \pmod{3} \):

Set \( x = 2 + 3t \).

Expand:

\[
(2 + 3t)^2 + 3(2 + 3t) + 17 = (4 + 12t + 9t^2) + (6 + 9t) + 17,
\]
\[
= 27 + 21t + 9t^2.
\]

Modulo 9:

\[
27 + 21t + 9t^2 \equiv 0 + 3t \pmod{9}.
\]

Thus:

\[
3t \equiv 0 \pmod{9}.
\]
\[
t \equiv 0 \pmod{3}.
\]

Thus, \( t = 0 \), so:

\[
x = 2 + 3 \times 0 = 2 \pmod{9}.
\]

The solutions modulo \( 9 \) are:

\[
x \equiv 2 \pmod{9}, \quad x \equiv 4 \pmod{9}.
\]

- **Step 3: Solve Modulo \( 5 \) and \( 7 \) — by Trial and Error**

We solve the congruences (B) and (C) by direct substitution.

Solve first :

\[
x^2 + 3x + 17 \equiv 0 \pmod{5}.
\]
Simplify:

\[
x^2 + 3x + 2 \equiv 0 \pmod{5}.
\]

Check each residue:

- \( x = 0 \): \( 0 + 0 + 2 = 2 \neq 0 \),
- \( x = 1 \): \( 1 + 3 + 2 = 6 \equiv 1 \),
- \( x = 2 \): \( 4 + 6 + 2 = 12 \equiv 2 \),
- \( x = 3 \): \( 9 + 9 + 2 = 20 \equiv 0 \) ✅
- \( x = 4 \): \( 16 + 12 + 2 = 30 \equiv 0 \) ✅

Thus:

\[
x \equiv 3, \quad x \equiv 4 \pmod{5}.
\]


Now solve modulo 7:

\[
x^2 + 3x + 17 \equiv 0 \pmod{7}.
\]
Simplify:

\[
x^2 + 3x + 3 \equiv 0 \pmod{7}.
\]

Check:

- \( x = 0 \): \( 0 + 0 + 3 = 3 \),
- \( x = 1 \): \( 1 + 3 + 3 = 7 \equiv 0 \) ✅
- \( x = 2 \): \( 4 + 6 + 3 = 13 \equiv 6 \),
- \( x = 3 \): \( 9 + 9 + 3 = 21 \equiv 0 \) ✅
- \( x = 4,5,6 \): nonzero.

Thus:

\[
x \equiv 1, \quad x \equiv 3 \pmod{7}.
\]


- **Step 4: Combine Solutions via CRT**

We now solve systems of the form:

- Pick one solution modulo 9 (either \( x \equiv 2 \) or \( x \equiv 4 \)),
- Combine with one solution modulo 5 (either \( x \equiv 3 \) or \( x \equiv 4 \)),
- Combine with one solution modulo 7 (either \( x \equiv 1 \) or \( x \equiv 3 \)).

Each choice leads to one solution modulo \( 315 \).

For example:

- Solve:

\[
\begin{aligned}
x &\equiv 2 \pmod{9},\\
x &\equiv 3 \pmod{5},\\
x &\equiv 1 \pmod{7}.
\end{aligned}
\]

Solving by successive substitutions or applying the CRT, we find:

\[
x \equiv 218 \pmod{315}.
\]

Similarly, solving:

\[
\begin{aligned}
x &\equiv 2 \pmod{9},\\
x &\equiv 3 \pmod{5},\\
x &\equiv 3 \pmod{7},
\end{aligned}
\]
we find:

\[
x \equiv 29 \pmod{315}.
\]

And similarly for other combinations.


- **Step 5: Final Solutions**

The complete list of solutions modulo \( 315 \) is:

\[
\boxed{29, 38, 94, 148, 164, 218, 274, 283}.
\]

Each corresponds to a different combination of solutions modulo 9, 5, and 7.

--- 

## Some Computational Validation

In order to validate our results and to facilitate future computations, we have included in the folder `src` a Python file implementing *Hensel's lemma*, called `Hensel.py`.

We can now use this tool to run some tests on our worked examples and confirm the correctness of our results.


*Example 1*: Solving \( f(x) = x^3 - 4x^2 + 5x - 6 \equiv 0 \pmod{27} \)

Recall that in the first example, we solved:

\[
f(x) = x^3 - 4x^2 + 5x - 6 \equiv 0 \pmod{27},
\]
and found the solution:

\[
x \equiv 3 \pmod{27}.
\]

To test this using our Python script, we execute the following command in the terminal:

```bash
python Hensel.py 3 3 1 -4 5 -6
```

Here:
- `3` is the prime modulus \( p \),
- `3` is the degree of the polynomial,
- `1 -4 5 -6` are the coefficients from highest to lowest degree.

Upon execution, we obtain:

```python
Using Hensel's Lemma to find solutions for: 
x^3 - 4x^2 + 5x - 6 mod 3^3 = 0
Solutions: [3.0]
```

which confirms the correctness of our earlier manual computation.


*Example 2*: Solving \( f(x) = x^2 + 3x + 17 \equiv 0 \pmod{9} \)

In the second example, we solved:

\[
x^2 + 3x + 17 \equiv 0 \pmod{9},
\]
and obtained solutions \( x \equiv 2 \pmod{9} \) and \( x \equiv 4 \pmod{9} \).

We test this with the following command:

```bash
python Hensel.py 3 2 1 3 17
```

where:
- `3` is the prime modulus,
- `2` is the degree,
- `1 3 17` are the coefficients.

The output is:

```python
Using Hensel's Lemma to find solutions for: 
x^2 + 3x + 17 mod 3^2 = 0
Solutions: [4.0, 2.0]
```

as expected.

Moreover, having already discussed the CRT, we can further validate our combined solution using SageMath.

For example, solving the system:

\[
\begin{aligned}
x &\equiv 2 \pmod{9},\\
x &\equiv 3 \pmod{5},\\
x &\equiv 1 \pmod{7},
\end{aligned}
\]
we may run:

```sage
crt([2, 3, 1], [9, 5, 7])
```

Since:

```sage
9*5*7 == 315
```
we confirm that the system is correctly set up.

The output is:

```
218
```
thus verifying that:

\[
x \equiv 218 \pmod{315}
\]
is indeed one of the solutions we previously computed manually.

---

## Wrap-up

In this first part, we developed the theory and practice of solving polynomial congruences, starting from linear congruences and progressing toward higher-degree cases using *Hensel’s Lemma* and the *CRT*.

We established:

- The fundamental criteria for solvability of linear congruences.
- The deep connection between modular equations and *linear Diophantine equations*.
- Techniques to solve polynomial congruences modulo prime powers via *Hensel’s lemma*.
- Methods to combine solutions for different prime factors via the *Chinese Remainder Theorem*.

Finally, through Python and SageMath implementations, we validated our theoretical results computationally, ensuring correctness and building tools for more advanced studies.
 
This concludes the first part of our exploration of congruences.  
In the next stages, we will extend these ideas toward non-linear congruences, modular arithmetic structures, and cryptographic applications.



