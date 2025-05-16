# Robust Secret Sharing via Gao Decoding

Secret Sharing is a foundational technique in cryptography for splitting a secret into multiple pieces (shares) such that only specific subsets of these shares can reconstruct the original secret. The classic example is **Shamir’s Secret Sharing** (SSS), which relies on polynomial interpolation over a finite field. While elegant and efficient, Shamir’s scheme is vulnerable to share corruption or adversarial tampering.

This report presents a robust alternative based on **Reed–Solomon decoding** and the **Gao decoding algorithm**, enabling reconstruction even in the presence of **missing and manipulated shares**. We provide a thorough explanation of the implementation and analyze its cryptographic strengths and trade-offs.

---

## Shamir’s Secret Sharing (SSS)


Shamir’s Secret Sharing is based on the principle that a polynomial of degree $t$ is uniquely determined by $t+1$ points. A secret is embedded as the constant term of a random degree-$t$ polynomial $f(x)$, and shares are evaluations of this polynomial at distinct non-zero points:

$$
\text{Share}_i = (x_i, f(x_i)), \quad i = 1,\ldots,N
$$

To recover the secret, any subset of $t+1$ shares suffices.

Standard SSS however comes with few limitations:

* All shares are received correctly.
* No shares are missing or manipulated.

In practice, especially in adversarial or noisy environments, this assumption often fails. SSS does **not** provide robustness against:

* **Erasures** (missing shares),
* **Errors** (maliciously modified shares).

Even a single incorrect share can cause interpolation to reconstruct the wrong secret.

So we are in need for *robust reconstruction*. In distributed or adversarial environments (e.g., secure MPC, blockchain consensus, fault-tolerant storage), it is critical to:

* Detect and correct errors,
* Tolerate missing data,
* Guarantee correct reconstruction under weaker assumptions.

This motivates the use of *error-correcting codes*, such as *Reed–Solomon codes*, and decoding techniques like *Gao decoding*, which extends SSS with robustness properties.

---

## Gao Decoding: A Reed–Solomon Based Approach

Gao decoding recovers the correct secret polynomial even when some shares are *missing* or *maliciously altered*, provided that the number of faulty shares is within bounds.

Let:

* $K$: degree of the secret (e.g., 1 in Shamir),
* $T$: number of random coefficients added (security threshold),
* $R = K + T$: required minimum number of honest shares,
* $e$: number of erroneous (manipulated) shares,
* $m$: number of missing shares.

The decoder tolerates errors as long as:

$$
R + m + 2e \leq N
$$

A high level idea:

1. **Interpolation**: Construct a polynomial $H(x)$ from the received shares (which may be incorrect).
2. **Known Structure**: Construct $F(x) = \prod (x - x_i)$ using all share positions.
3. **Extended Euclidean Algorithm (EEA)**:

   * Apply EEA to $(F, H)$ to find polynomials $G(x), T(x)$ such that:

     $$
     R_0 = G(x) \cdot T(x), \quad \text{and} \quad \deg(G) < K, \deg(T) \leq e
     $$
4. **Error Locator**: $T(x)$ has roots at corrupted $x_i$. These can be used to **identify bad shares**.
5. **Secret Recovery**: Evaluate $G(0)$ to retrieve the original secret.

You can find the code into the `src/ReedGao.py`. Below we explain it briefly. Dont forget that you need *some* mathematical background to keep up. 


* Operates over $\mathbb{F}_{433}$, a small prime field.
* Implements modular addition, subtraction, multiplication, inversion, and division.
* Implements standard polynomial operations: addition, multiplication, division, scalar multiplication.
* Uses `canonical` representation to trim trailing zeros.
* Division is implemented using classical long division with normalization by leading coefficient.
* Computes the unique polynomial of degree $\leq t$ passing through $t+1$ given points.
* Implements the decoding algorithm using the extended Euclidean algorithm for polynomials.
* Performs decoding of possibly faulty shares and returns the original polynomial (if recovery is possible) along with an error locator.

Application to Shamir's Scheme : 
* `shamir_share(secret)` creates a polynomial of degree $T$, embeds the secret as its constant term, and evaluates it at $N$ points.
* `shamir_robust_reconstruct(shares)` applies Gao decoding to reconstruct the secret even with up to $m$ missing and $e$ faulty shares.

 A naive cryptographic analysis could be the following: 

(+) **Error Correction**: Can correct up to $e$ manipulated shares and detect their locations.
(+) **Erasures**: Tolerates missing shares.
(+) **Security**: Maintains $T$-privacy; any $\leq T$ shares reveal no information.
(+) **Robustness**: Suitable for hostile environments (active adversaries, faulty nodes).


(-) **Complexity**: Reconstruction involves polynomial division and EEA, which is more complex than naive Lagrange interpolation.
(-) **Performance**: Overhead in decoding logic and memory usage due to polynomial manipulation.
(-) **Finite Field Size**: The field size must be sufficiently large to support the desired number of shares and operations without collisions.


| Feature                       | Shamir SSS             | Robust SSS (Gao)    |
| ----------------------------- | ---------------------- | ------------------- |
| Tolerance to missing shares   | No                     | Yes                 |
| Tolerance to incorrect shares | No                     | Yes (up to bound)   |
| Fault localization            | No                     | Yes                 |
| Reconstruction method         | Lagrange interpolation | EEA-based decoding  |
| Complexity                    | Low                    | Moderate            |
| Use case                      | Honest participants    | Adversarial setting |


While Shamir’s Secret Sharing provides efficient and elegant threshold secret distribution, it lacks robustness against faulty or malicious inputs. This implementation demonstrates how *Gao decoding*, adapted from *Reed–Solomon error correction*, enhances SSS by enabling recovery even under adversarial conditions.

Such robust schemes are critical in real-world cryptographic applications, including:

* Secure multiparty computation (MPC),
* Blockchain validator security,
* Long-term archival with fault-tolerance,
* Adversarial distributed systems.
