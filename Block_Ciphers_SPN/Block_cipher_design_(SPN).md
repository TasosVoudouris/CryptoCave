# Block Ciphers Designs (SPN Part)
## Table of Contents

- [Block Ciphers Designs (SPN Part)](#block-ciphers-designs-spn-part)
  - [Table of Contents](#table-of-contents)
  - [What is a Block Cipher?](#what-is-a-block-cipher)
  - [Confusion and Diffusion](#confusion-and-diffusion)
  - [Cryptanalytic Considerations](#cryptanalytic-considerations)
  - [Block Cipher Construction Paradigms](#block-cipher-construction-paradigms)
    - [Designing a Block Cipher: Round Function \& Key Schedule](#designing-a-block-cipher-round-function--key-schedule)
      - [**1. The Key Schedule**](#1-the-key-schedule)
      - [**2. The Round Function**](#2-the-round-function)
      - [**Remark on Reversibility**](#remark-on-reversibility)
    - [Substitution Permutation Network (SPN)](#substitution-permutation-network-spn)
  - [SPN Core Components](#spn-core-components)
    - [Bit-Level Utilities](#bit-level-utilities)
    - [Substitution and Permutation Functions](#substitution-and-permutation-functions)
    - [Testing the Components](#testing-the-components)
    - [Key Scheduling and Message Setup](#key-scheduling-and-message-setup)
    - [Define the Plaintext Message](#define-the-plaintext-message)
  - [Defining the S-box and P-box](#defining-the-s-box-and-p-box)
    - [🔁 S-box Mapping ( \\pi\_S )](#-s-box-mapping--pi_s-)
    - [🔀 P-box Mapping ( \\pi\_P )](#-p-box-mapping--pi_p-)
  - [Implementing the Full SPN Encryption](#implementing-the-full-spn-encryption)
    - [`spn_network()` function](#spn_network-function)
- [Conclusion](#conclusion)
    - [Core Components](#core-components)
    - [SPN Encryption Logic](#spn-encryption-logic)
      - [1. **Functional Form: `spn_network()`**](#1-functional-form-spn_network)
      - [2. **Object-Oriented Form: `SPN` Class**](#2-object-oriented-form-spn-class)
    - [Test Setup](#test-setup)

## What is a Block Cipher?

A **block cipher** is a symmetric encryption algorithm that operates on fixed-size blocks of data, typically 64 or 128 bits. It transforms each block of plaintext into a block of ciphertext of the same size using a secret key. The two main parameters that characterize a block cipher are:

- **Block size** \( b \): The number of bits processed at a time (e.g., 128 bits in AES).
- **Key size** \( k \): The length of the secret key used for encryption and decryption.

---

## Confusion and Diffusion

To ensure cryptographic security, a block cipher must provide two essential properties:

- **Confusion**: The relationship between the ciphertext and the encryption key should be complex and unintelligible. Specifically, the ciphertext statistics should depend on the plaintext statistics in a way that is too intricate to be exploited by a cryptanalyst.
  
- **Diffusion**: Each bit of the plaintext (and of the key) should influence many bits of the ciphertext. This helps spread the influence of individual bits throughout the output, reducing statistical patterns.

> For more on these principles, see [Wikipedia – Confusion and Diffusion](https://en.wikipedia.org/wiki/Confusion_and_diffusion).

---

## Cryptanalytic Considerations

When analyzing or attempting to break a block cipher, three key resource parameters are considered:

- **Time**: The computational effort (e.g., number of operations) required for a successful attack.
- **Memory**: The amount of storage needed during the attack (often in time-memory tradeoff scenarios).
- **Data**: The volume of data required, such as known ciphertexts or known plaintext-ciphertext pairs.

In most cases, an attacker's objective is to recover the secret key. For a well-designed cipher with key size \( k \), any attack should ideally require approximately \( 2^k \) operations — a brute-force effort.

We will examine these parameters more closely when we explore practical cryptanalysis techniques.

---

## Block Cipher Construction Paradigms

There are two major structural frameworks commonly used to design block ciphers:

- **Feistel Networks** (e.g., DES): A structure where the input block is split and processed through multiple rounds, allowing encryption and decryption to use the same components.
  
- **Substitution–Permutation Networks (SPN)** (e.g., AES): A structure based on repeated application of substitution (non-linear) and permutation (linear diffusion) layers.

Both paradigms aim to achieve strong confusion and diffusion through iterative transformations.

---

### Designing a Block Cipher: Round Function & Key Schedule

Designing a block cipher requires defining two essential components:

#### **1. The Key Schedule**

Let \( K \) be the secret master key.  
The key schedule algorithm derives a sequence of \( N \) round keys:

\[
K^1, K^2, \dots, K^N
\]

These round keys are used in each round of the cipher to introduce key-dependent transformations.

![Key Schedule Overview](images/keyschedule.png)

This diagram shows how the key schedule derives multiple round keys from the main key. These keys are then used independently across each round.

---

#### **2. The Round Function**

Let \( w^{r-1} \) denote the state of the block cipher after round \( r-1 \).  
Each round applies a transformation function \( g \) using the round key \( K^r \):

\[
w^r = g(w^{r-1}, K^r)
\]

This function defines how the state evolves during encryption.

---

#### **Remark on Reversibility**

To support decryption, the round transformation \( g \) must be **reversible**. This typically means:
- For **Substitution-Permutation Networks (SPNs)** like **AES**, \( g \) must be **invertible** — we must be able to define a function \( g^{-1} \) such that:

\[
g^{-1}(g(w, k), k) = w
\]

- For **Feistel networks** like **DES**, this constraint is relaxed:  
  Even if the round function \( F \) is not invertible, the **Feistel structure itself** guarantees that the overall cipher remains invertible.

Hence, while this general framework applies to all block ciphers, **the requirement for \( g \) to be injective holds strictly for SPN-based designs** — not for Feistel constructions.

---

### Substitution Permutation Network (SPN)

Let  
- \( l, m \in \mathbb{Z}_+ \) be two integers. \( l\cdot m \) is the block length of the cipher \( \Rightarrow \mathcal{M} = \mathcal{C} = \{0, 1\}^{lm}\)
- \( \pi_S: \{0, 1\}^l \to \{0, 1\}^l \) be the **S-box** (substitution box). It replaces \( l \) bits with a different set of \( l \) bits and provides the **confusion** property.
- \( \pi_P: \{1, \dots, l\cdot m\} \to \{1, \dots, l \cdot m \} \) be a permutation function. It reorders the \( lm \) bits and provides the **diffusion** property.

The SPN has \( N \) rounds. Except for the last round we will perform substitution \(\to\) permutation \(\to\) add key.

> **Note:**  
> - The S-box and P-box do not alone provide security, as they are publicly known and reversible.
> - The XOR operation with the **secret key** is what introduces cryptographic strength.

![SPN Layered Architecture](images/sp.png)

The above diagram illustrates the internal layering of an SPN cipher: each round consists of substitution, permutation, and key addition. This layering helps achieve both diffusion and confusion over multiple iterations.

![SPN Round-by-Round Detail](images/encryption.png)

This detailed diagram shows how the SPN works at the bit and sub-block level across multiple rounds. It highlights how bits are substituted, permuted, and then combined with round keys, providing strong avalanche effects.

## SPN Core Components
To understand and implement a Substitution–Permutation Network (SPN), we begin by defining a few helper functions that operate on bits and provide utility for substitution and permutation operations. These are fundamental to modeling the internal structure of SPN ciphers programmatically.

### Bit-Level Utilities

```python
# Helper functions


def bit_parity(x: int):
    """
    Computes the bit parity (i.e., XOR of all bits) of an integer.
    Returns 1 if the number of 1s in the binary representation is odd, else 0.
    """
    t = 0
    while x != 0:
        t = t ^ (x & 1)
        x >>= 1
    return t


def get_bit(x: int, i: int, n: int):
    """
    Gets the i-th bit (left-to-right, 0-indexed) of an n-bit number.
    Example: get_bit(0b1010, 1, 4) returns 0 (second bit from the left)
    example for n_bits = 5
    x = 0 1 0 1 0
    i = 0 1 2 3 4
    """
    return (x >> (n - 1 - i)) & 1


def set_bit(x: int, i: int, n: int, b: int):
    """
    sets the `i`th bit to `b` of an n_bits-bit number (0 or 1).
    """
    if b == 1:
        return x | (1 << (n - 1 - i))
    else:
        return x & ~int((1 << (n - 1 - i)))


def inverse_sbox(S: list):
    """
    Computes the inverse of an S-box (substitution table).

    Input:
    S: {list} -- sbox
    Return
    {list} -- the inverse of the sbox
    """
    S_ = [-1] * len(S)
    for i, entry in enumerate(S):
        S_[entry] = i
    return S_
```

### Substitution and Permutation Functions
We now define the essential SPN operations:

```python
# Substitute and permute


def substitute(x: int, sbox: list, l: int) -> int:
    """


    Applies S-box substitution to an input integer `x`.
    Splits `x` into l-bit chunks and replaces each chunk using the S-box.
    Takes a 2**n bit number x and substitutes n-bit parts according to the n-bit sbox
    Arguments
        x: {int} --  input number of size 2**n bits
        sbox: {Sbox} -- Sbox with input entries of size n bits
        l: {int} -- Sbox input size in bits
    Returns
        {int} -- output sboxed
    """
    word_size = 1 << l
    mask = (1 << l) - 1
    y = 0
    for i in range(0, word_size, l):  # Steps of n-bits
        y = y << l  # Shift 'l' positions to make space for l-bit sbox number
        idx = (x >> (word_size - i - l)) & mask  # Get n-bit index in the sbox
        y = y | sbox[idx]  # "append" the bit from x
    return y


def permute(x: int, pbox: list, n: int) -> int:
    """
    Takes a n-bit int x and permutes the bits from it according to the pbox
    Arguments
        x: {int}  -- n-bit int
        pbox: {list} -- list of integers of length n
        n: int -- number of bits of x
    Return:
        {int}
    """
    y = 0
    for p in pbox:
        y = y << 1  # shift to make space for LSB
        y = y ^ get_bit(x, p, n)  # "append" the p'th bit from x
    return y
```

### Testing the Components
We conclude this part with a few test examples to validate our helper functions:

```python
# Examples
print(bit_parity(0b1010))  # 0
print(get_bit(0b1010, 1, 4))  # Output: 0 (2nd bit from left in 4-bit word)
print(set_bit(0b1010, i=1, n=4, b=1))  # Output: 14 (binary: 1110)
print(set_bit(0b1010, i=2, n=4, b=0))  # Output: 8  (binary: 1000)
```
These operations form the foundation of a simplified SPN cipher model.

### Key Scheduling and Message Setup

Before we proceed to the full encryption process, we need to prepare our round keys and define a test message.

In this simplified SPN setup, we use a fixed 32-bit master key and derive 5 round keys of 16 bits each by sliding a 16-bit window with a 4-bit step across the key.

```python
# Define a 32-bit master key
K = 0b0011_1010_1001_0100_1101_0110_0011_1111

# Derive five 16-bit round keys using a sliding window
Ks = [
    int(bin(K)[2:].zfill(32)[4 * r : 4 * r + 16], 2)
    for r in range(5)
]

# Display the round keys in binary
print([bin(Ki)[2:].zfill(16) for Ki in Ks])
```
This results in the following round keys (as binary strings): `['0011101010010100', '1010100101001101', '1001010011010110', '0100110101100011', '1101011000111111']`
The window shifts by 4 bits each time (not 16!) to increase diffusion and ensure round keys overlap — a classic SPN design trick.

### Define the Plaintext Message
Now let’s define a 16-bit plaintext message that we will use for encryption and decryption:

```python
# Define a 16-bit message
m = 0b0010_0110_1011_0111
```
## Defining the S-box and P-box

To implement the **Substitution–Permutation Network (SPN)**, we need to define the two main cryptographic components:

- An **S-box** (Substitution Box) — introduces non-linearity (**confusion**)
- A **P-box** (Permutation Box) — rearranges bits (**diffusion**)

---

### 🔁 S-box Mapping \( \pi_S \)

This table shows how each 4-bit nibble \( z \in \{0, 1, ..., 15\} \) is substituted:

| \( z \)         | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|-----------------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| \( \pi_S(z) \)  | E | 4 | D | 1 | 2 | F | B | 8 | 3 | A | 6 | C | 5 | 9 | 0 | 7 |

This substitution layer provides **confusion** by replacing each 4-bit input with a 4-bit output using a nonlinear mapping.

---

### 🔀 P-box Mapping \( \pi_P \)

This bit-level permutation rearranges the output bits of the S-box:

| \( z \)         | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|-----------------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| \( \pi_P(z) \)  | 0 | 4 | 8 | 12| 1 | 5 | 9 | 13| 2 | 6 | 10| 14| 3 | 7 | 11| 15 |

The P-box ensures **diffusion** by redistributing the bits to different positions after substitution.


We define these mappings in Python as:

```python
# Define the S-box and P-box
S = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
```

We can now apply the substitution to a test 16-bit input: `hex(substitute(0x0123, S, 4))` with output: `'0xe4d1'
`

---

## Implementing the Full SPN Encryption

With our **S-box**, **P-box**, and bit manipulation functions implemented, we now proceed to define the full **SPN encryption network**.

This function performs multi-round encryption using substitution, permutation, and key addition at each round.

---

### `spn_network()` function

```python
def spn_network(m: int, K: int, S: list, P: list, n: int = 4, word_size: int = 16, verbose: bool = False):
    # Derive round keys: 5 keys of 16 bits from the 32-bit master key
    Ks = [K >> i * 4 & 0xFFFF for i in range(4, -1, -1)]

    w = m
    for i in range(len(Ks) - 2):  # First N-1 rounds
        u = w ^ Ks[i]             # Add round key
        v = substitute(u, S, n)   # Substitution layer
        w = permute(v, P, word_size)  # Permutation layer

        if verbose:
            print(f"K{i}: ", bin(Ks[i])[2:].zfill(16))
            print(f"u{i}: ", bin(u)[2:].zfill(16))
            print(f"v{i}: ", bin(v)[2:].zfill(16))
            print(f"w{i}: ", bin(w)[2:].zfill(16))

    # Final round: only substitute + add key (no permutation)
    u = w ^ Ks[-2]
    v = substitute(u, S, n)
    y = v ^ Ks[-1]

    if verbose:
        print(f"K{i+1}: ", bin(Ks[i + 1])[2:].zfill(16))
        print(f"u{i+1}: ", bin(u)[2:].zfill(16))
        print(f"v{i+1}: ", bin(v)[2:].zfill(16))
        print(f"K{i+2}: ", bin(Ks[i + 2])[2:].zfill(16))

    return y

spn_network(m, K, S, P, verbose=True)
```
This returns the length (in bits) of the master key $K$. For example, a 32-bit key will return `32`. This `spn_network` function encapsulates the round-based logic of an SPN cipher.

Full implementation with an integrated class: 

```python
# Helper functions
def bit_parity(x: int):
    """
    Bit parity of a number
    """
    t = 0
    while x != 0:
        t = t ^ (x & 1)
        x >>= 1
    return t


def get_bit(x: int, i: int, n: int):
    """
    Gets the ith bit of an n-bit number
    n_bits = 5
    x = 0 1 0 1 0
    i = 0 1 2 3 4
    """
    return (x >> (n - 1 - i)) & 1


def set_bit(x: int, i: int, n: int, b: int):
    """
    sets the `i`th bit to `b` of an n_bits-bit numebr
    """
    if b == 1:
        return x | (1 << (n - 1 - i))
    else:
        return x & ~int((1 << (n - 1 - i)))


def inverse_sbox(S: list):
    """
    Input:
    S: {list} -- sbox
    Return
    {list} -- the inverse of the sbox
    """
    S_ = [-1] * len(S)
    for i, entry in enumerate(S):
        S_[entry] = i
    return S_

def substitute(x: int, sbox: list, l: int) -> int:
    """
    Takes a 2**n bit number x and substitutes n-bit parts according to the n-bit sbox
    Arguments
        x: {int} --  input number of size 2**n bits
        sbox: {Sbox} -- Sbox with input entries of size n bits
        l: {int} -- Sbox input size in bits
    Returns
        {int} -- output sboxed
    """
    word_size = 1 << l
    mask = (1 << l) - 1
    y = 0
    for i in range(0, word_size, l):  # Steps of n-bits
        y = y << l  # Shift 'l' positions to make space for l-bit sbox number
        idx = (x >> (word_size - i - l)) & mask  # Get n-bit index in the sbox
        y = y | sbox[idx]  # "append" the bit from x
    return y


def permute(x: int, pbox: list, n: int) -> int:
    """
    Takes a n-bit int x and permutes the bits from it according to the pbox
    Arguments
        x: {int}  -- n-bit int
        pbox: {list} -- list of integers of length n
        n: int -- number of bits of x
    Return:
        {int}
    """
    y = 0
    for p in pbox:
        y = y << 1  # shift to make space for LSB
        y = y ^ get_bit(x, p, n)  # "append" the p'th bit from x
    return y


def spn_network(m: int, K: int, S: list, P: list, n: int = 4, word_size: int = 16, verbose: bool = False):
    # Derive round keys: 5 keys of 16 bits from the 32-bit master key
    Ks = [K >> i * 4 & 0xFFFF for i in range(4, -1, -1)]

    w = m
    for i in range(len(Ks) - 2):  # First N-1 rounds
        u = w ^ Ks[i]             # Add round key
        v = substitute(u, S, n)   # Substitution layer
        w = permute(v, P, word_size)  # Permutation layer

        if verbose:
            print(f"K{i}: ", bin(Ks[i])[2:].zfill(16))
            print(f"u{i}: ", bin(u)[2:].zfill(16))
            print(f"v{i}: ", bin(v)[2:].zfill(16))
            print(f"w{i}: ", bin(w)[2:].zfill(16))

    # Final round: only substitute + add key (no permutation)
    u = w ^ Ks[-2]
    v = substitute(u, S, n)
    y = v ^ Ks[-1]

    if verbose:
        print(f"K{i+1}: ", bin(Ks[i + 1])[2:].zfill(16))
        print(f"u{i+1}: ", bin(u)[2:].zfill(16))
        print(f"v{i+1}: ", bin(v)[2:].zfill(16))
        print(f"K{i+2}: ", bin(Ks[i + 2])[2:].zfill(16))

    return y

class SPN:
    def __init__(self, sbox: list, pbox: list, block_size: int = 16, sbox_input_size: int = 4):
        self.sbox = sbox
        self.sbox_ = inverse_sbox(sbox)
        self.pbox = pbox
        self.block_size = block_size
        self.l = sbox_input_size

    def key_schedule(self, k: int) -> list:
        return [k >> i * 4 & 0xFFFF for i in range(4, -1, -1)]

    def encrypt(self, m: int, k: int) -> int:
        ks = self.key_schedule(k)

        w = m
        for i in range(len(ks) - 2):
            u = w ^ ks[i]
            v = substitute(u, self.sbox, self.l)
            w = permute(v, self.pbox, self.block_size)

        u = w ^ ks[-2]
        v = substitute(u, S, self.l)
        y = v ^ ks[-1]

        return y

    def decrypt(self, c: int, k: int) -> int:

        ks = self.key_schedule(k)

        v = ks[-1] ^ c
        u = substitute(v, self.sbox_, self.l)
        w = ks[-2] ^ u

        for ki in ks[::-1][2:]:
            v = permute(w, self.pbox, self.block_size)
            u = substitute(v, self.sbox_, self.l)
            w = u ^ ki
        return w

S = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
m = 0b0010_0110_1011_0111  # message
K = 0b0011_1010_1001_0100_1101_0110_0011_1111
print(K.bit_length())

spn_network(m, K, S, P, verbose=True)
spn = SPN(S, P)
c = spn.encrypt(m, K)
print(c)

m == spn.decrypt(c, K)
```

---

# Conclusion

In this section, we implemented a *lightweight* block cipher using the **Substitution–Permutation Network (SPN)** paradigm, showcasing a clean and educational design for symmetric encryption.

---

### Core Components

We defined several utility functions essential for bit-level manipulation:
- `bit_parity`, `get_bit`, and `set_bit`: Handle individual bit processing.
- `substitute`: Applies an S-box substitution to blocks of bits.
- `permute`: Reorders bits based on a permutation (P-box).
- `inverse_sbox`: Automatically derives the inverse of a given S-box.

---

### SPN Encryption Logic

The core encryption logic is implemented in two ways:

#### 1. **Functional Form: `spn_network()`**
- Takes plaintext, a 32-bit master key, S-box, and P-box.
- Derives 5 round keys from the key schedule.
- Performs:
  - XOR with round key
  - Substitution
  - Permutation
  - A final round with substitution and key addition only

It optionally prints each round’s internal values for verbose tracing and debugging.

#### 2. **Object-Oriented Form: `SPN` Class**
- Encapsulates the cipher logic with attributes for the S-box, P-box, and block size.
- Includes:
  - `key_schedule()`: Generates round keys from the master key.
  - `encrypt()`: Follows the SPN logic across multiple rounds.
  - `decrypt()`: Performs the inverse operations using the inverse S-box and reversed key schedule.

---

### Test Setup

We tested the implementation with the following parameters:
- A **fixed 16-bit message**: `0b0010011010110111`
- A **fixed 32-bit key**: `0b00111010100101001101011000111111`
- A 4-bit S-box and a 16-bit P-box:

```python
  S = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
  P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
```
The test included:

- Encrypting the plaintext using both the standalone `spn_network()` function and the SPN class.

- Verifying correct decryption, i.e., `decrypt(encrypt(m)) == m`.

The encryption and decryption passed all tests. This confirms that:

- The round transformations correctly apply confusion and diffusion.

- The key schedule works consistently across both implementations.

- The cipher is logically reversible, as required for symmetric-key encryption.

This implementation provides a fully functional educational SPN cipher, ideal for further exploration of cryptanalysis, lightweight crypto, or even hardware modeling of symmetric encryption schemes.

