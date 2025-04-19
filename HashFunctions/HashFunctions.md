# Hash Functions (A primer)

- [Hash Functions (A primer)](#hash-functions-a-primer)
  - [Introduction to Hash Functions](#introduction-to-hash-functions)
    - [Security Properties](#security-properties)
    - [Python Examples Using `hashlib`](#python-examples-using-hashlib)
  - [Hash Output Lengths (in bytes)](#hash-output-lengths-in-bytes)
- [A non-preimage resistant hash function](#a-non-preimage-resistant-hash-function)
  - [Python Example Demonstration](#python-example-demonstration)
- [A Hash Function that is not second preimage resistant](#a-hash-function-that-is-not-second-preimage-resistant)
  - [Finding actually a Second Preimage](#finding-actually-a-second-preimage)
  - [Python Example Demonstration](#python-example-demonstration-1)
- [Collision Attack](#collision-attack)
  - [Python Example Demonstration:](#python-example-demonstration-2)
  - [Caesar Cipher as a Hash Function: Preimage Resistance](#caesar-cipher-as-a-hash-function-preimage-resistance)
- [Another hash function that is not second preimage resistant](#another-hash-function-that-is-not-second-preimage-resistant)
- [Finding a Collision in a Truncated MD5 Hash Function](#finding-a-collision-in-a-truncated-md5-hash-function)
- [Conclusion](#conclusion)



## Introduction to Hash Functions

A **hash function** is a mathematical algorithm that takes input data of arbitrary length and maps it to an output of fixed length.

In software engineering and cryptographic applications, hash functions typically accept byte strings as input and produce a fixed-size byte string as output.

### Security Properties

Cryptographically secure hash functions must satisfy the following three important security properties:

- **Preimage Resistance:**  
  Given a hash value \( h \), it should be computationally infeasible to find an input \( x \) such that \( H(x) = h \).

- **Second Preimage Resistance:**  
  Given an input \( x \) and its corresponding hash value \( h = H(x) \), it should be computationally infeasible to find a different input \( x' \neq x \) such that \( H(x') = h \).

- **Collision Resistance:**  
  It should be computationally infeasible to find any two distinct inputs \( a \neq b \) such that \( H(a) = H(b) \).

### Python Examples Using `hashlib`

The Python library `hashlib` provides implementations for various popular hash functions, such as MD5, SHA-1, and SHA-256.

**MD5 Example:**  
```python
import hashlib

msg = b'Hello'
hash_md5 = hashlib.md5(msg).digest()
hash_md5
# Output: b"\x8b\x1a\x99S\xc4a\x12\x96\xa8'\xab\xf8\xc4x\x04\xd7"

hash_md5.hex()  # Convert raw bytes to hex representation
# Output: '8b1a9953c4611296a827abf8c47804d7'
```

**SHA-256 Example:**  
```python
import hashlib

msg = b'Hello'
hash_sha256 = hashlib.sha256(msg).hexdigest()
hash_sha256
# Output: '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969'
```

**SHA-1 Example:**  
```python
import hashlib

msg = b'Hello'
hash_sha1 = hashlib.sha1(msg).hexdigest()
hash_sha1
# Output: 'f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0'
```

## Hash Output Lengths (in bytes)

```python
len(hashlib.sha1(msg).digest())     # SHA-1 output length
# Output: 20 (160 bits / 8 bits per byte)

len(hashlib.sha256(msg).digest())   # SHA-256 output length
# Output: 32 (256 bits / 8 bits per byte)

len(hashlib.md5(msg).digest())      # MD5 output length
# Output: 16 (128 bits / 8 bits per byte)
```

Note the following: 

- **MD5** is considered cryptographically broken due to vulnerabilities in collision resistance and thus should not be used for security-critical purposes.
- **SHA-1** is also considered insecure for collision resistance. Newer applications should prefer **SHA-256** or **SHA-3** family algorithms, as these provide higher levels of security.

---

# A non-preimage resistant hash function 

Consider the following hash function \( H(x) \), defined by a simple linear relationship:

\[
H(x) = a \cdot x + b
\]

> Let's test its resistance!

Given a hash value \( H(x) \), it's straightforward to reverse-engineer the original input \( x \) using basic algebra:

\[
x = \frac{H(x) - b}{a}
\]

> Why is this problematic?

- A hash function is considered **preimage resistant** if, given a hash value \( H(x) \), it is **computationally infeasible** to find an input \( x \) such that \( H(x) \) equals this value.
- The given hash function is **linear** and **invertible**, which means it is easy and efficient to reverse. Thus, it **fails** the preimage resistance property required for cryptographic security.

## Python Example Demonstration

```python
def H(x, a, b):
    return a * x + b

def reverse_H(h, a, b):
    return (h - b) // a

# Example parameters
a = 11
b = -977
x = 1337

# Calculating hash
h = H(x, a, b)

# Reversing the hash
x_recovered = reverse_H(h, a, b)

print(f'hash = {h}')
print(f'reversed hash (recovered input) = {x_recovered}')
print(f'real input = {x}')
```

We have the following output:

```
hash = 13730
reversed hash (recovered input) = 1337
real input = 1337
```

# A Hash Function that is not second preimage resistant

Consider a hash function that calculates the hash of input \( x \) as follows:

\[
H(x) = \text{digit\_sum}(x)
\]

In other words, the hash value is simply the sum of the ASCII values of all characters in the input string.

> Let's test its resistance!

Consider the input string `"hello"`:

- Calculate the hash:

\[
H(\text{"hello"}) = \text{ord('h') + ord('e') + ord('l') + ord('l') + ord('o')} = 104 + 101 + 108 + 108 + 111 = 532
\]

Thus:

\[
H(\text{"hello"}) = 532 = 0x214 = \texttt{b'\textbackslash x02\textbackslash x14'}
\]


## Finding actually a Second Preimage

The task is to find another input string \( x' \) such that:

\[
H(x') = 532
\]

This task is **trivial** because **any permutation (anagram)** of the letters in `"hello"` (such as `"loleh"`, `"ohlle"`, etc.) or even completely unrelated strings can yield the **same hash**.

Examples include:

- \( H(\text{"hello"}) = 532 \)
- \( H(\text{"ehllo"}) = 532 \)
- \( H(\text{"helol"}) = 532 \)

Moreover, completely different character sets may also sum to the same value. For example, `"kbqgA."` also sums to 532, illustrating how easy it is to find a second preimage.

> Why is this problematic?

- A **second preimage-resistant** hash function must make it **computationally infeasible** to find another distinct input \( x' \neq x \) that produces the same hash value \( H(x) \).
- Because the defined hash function is **order-independent and simplistic**, it clearly fails the second preimage resistance property.

## Python Example Demonstration

```python
def H(x):
    return sum(ord(c) for c in x)

x1 = 'crypto'
x2 = 'crptoy'
x3 = 'ytcopr'

# Ensure all inputs are distinct
assert x1 != x2 and x2 != x3 and x1 != x3

h1 = H(x1)
h2 = H(x2)
h3 = H(x3)

# Verify that all hashes are equal
assert h1 == h2 == h3

print(f'H("{x1}") = {hex(h1)}')
print(f'H("{x2}") = {hex(h2)}')
print(f'H("{x3}") = {hex(h3)}')
```

We have the following output: 
```
H("crypto") = 0x2a1
H("crptoy") = 0x2a1
H("ytcopr") = 0x2a1
```

In *cryptographic hash functions*, it must be practically impossible to find distinct inputs producing the same hash, ensuring robustness against collision-based attacks.

---

# Collision Attack

It is well-known that **MD5** collisions have been demonstrated in practice. Specifically, consider the MD5 hashes of the following two distinct images:

| Plane                           | Ship                          |
|-----------------------------------------------|----------------------------------------------|
| ![Plane](images/plane.jpg)                           | ![Ship](images/ship.jpg)                            |

## Python Example Demonstration:

```python
import hashlib

with open('plane.jpg', 'rb') as f:
    plane_hash = hashlib.md5(f.read()).hexdigest()

with open('ship.jpg', 'rb') as f:
    ship_hash = hashlib.md5(f.read()).hexdigest()

print(f'plane hash: {plane_hash}')
print(f'ship hash:  {ship_hash}')
```

We have the following output:
```
plane hash: 253dd04e87492e4fc3471de5e776bc3d
ship hash:  253dd04e87492e4fc3471de5e776bc3d
```

- We successfully demonstrated an MD5 collision—two *distinct inputs* (images) produce the *same hash*.
- This explicitly shows that **MD5** is *not collision-resistant* and therefore *unsuitable for cryptographic purposes*.

Keep in mind the following:
> Simply renaming a file from `.jpg` to `.png` will not change its MD5 hash, as the hash depends only on the file's binary content, not its name or extension. However, if you convert the image format from JPEG to PNG (i.e., re-saving or exporting it in a different image format), the internal binary data will change, resulting in a different MD5 hash.
---

## Caesar Cipher as a Hash Function: Preimage Resistance

Consider using the **Caesar cipher** with a fixed shift (**key = 17**) as a **hash function**. Such a hash function computes the hash \(H(x)\) by encrypting the input text with this Caesar shift.

Cosnider the following example: 
- Input: `'a'`  
  Hash: \(H('a') = 'r'\)

- Input: `'lower'`  
  Hash: \(H('lower') = 'cfnvi'\)

> Is this hash function preimage resistant?

**No**, this hash function is **not preimage resistant**.

Since the Caesar cipher is a *reversible encryption method*, it is straightforward to *decrypt* the hash output and recover the original input.

Specifically, given the hash output `'cfnvi'`, we can recover the original plaintext as follows:

\[
\text{CaesarDecrypt}('cfnvi', 17) = 'lower'
\]

Thus, the hash function \(H\) is easily **invertible**.

> Why is this a problem?

- A cryptographic hash function must be **preimage resistant**: given a hash output \(H(x)\), it should be **computationally infeasible** to recover the original input \(x\).

- The Caesar cipher is **deterministic** and **fully reversible**, which directly violates preimage resistance.

Therefore, **using Caesar cipher encryption as a cryptographic hash function is insecure**.


Cryptographically secure hash functions (e.g., **SHA-256**, **SHA-3**) are explicitly designed to ensure **irreversibility** and strong resistance to inversion attacks.

---

# Another hash function that is not second preimage resistant

Consider a hash function \(H\) defined by applying the bitwise operation **AND** with the hexadecimal constant \(0xAD\) to each byte of the input.

Formally, the hash function can be expressed as:

\[
H(x) = x \;\&\; 0xAD
\]

where the **bitwise AND** operation is applied individually to each byte of the input string.

Consider the following example:

Given the input string \(x = \text{'f1nd\_m3'}\):

\[
H(\text{'f1nd\_m3'}) = \text{'\$!,\$\textbackslash r-!'}
\]

Verification:

- \(\text{ord}('f') \;\&\; 0xAD = 102 \;\&\; 173 = 36 = \text{ord}('\$')\)
- \(\text{ord}('1') \;\&\; 0xAD = 49 \;\&\; 173 = 33 = \text{ord}('!')\)

Thus, the hash output for \(\text{'f1nd\_m3'}\) is indeed \(\text{'\$!,\$\textbackslash r-!'}\).


The hash function described above *does not satisfy* the second preimage resistance property.

Remember the definition: 

>A hash function is said to be **second preimage resistant** if, given an input \(x\) and its hash \(H(x)\), it is computationally infeasible to find another input \(x' \neq x\) such that: H(x') = H(x). 


However, due to the simplicity and the bitwise nature of the given function, finding such an input \(x'\) is trivial. Each output byte only depends on a bitwise AND with a fixed constant, resulting in multiple potential inputs for each output byte.

Below is a Python script demonstrating how one can easily find a second preimage:

```python
def H(x):
    return bytes([b & 0xad for b in x])

x = b'f1nd_m3'
h = H(x)

# Attempting to find a second preimage for the given hash
inp = b''
for hb in h:
    for b in range(256):
        if b & 0xad == hb:
            inp += bytes([b])
            break  # Found a valid byte, move to the next hash byte

print(f'H({x}) = {H(x)}')
print(f'H({inp}) = {H(inp)}')
```

We have the following output:

```
H(b'f1nd_m3') = b'$!,$\r-!'
H(b'vs~v_\x7fs') = b'$!,$\r-!'
```

This demonstrates explicitly that the inputs `b'f1nd_m3'` and `b'vs~v_\x7fs'` produce the same hash value, illustrating that the function is **not second preimage resistant**.

Due to the ease of finding multiple inputs producing identical hashes, this hash function is unsuitable for cryptographic purposes, as it fails to provide the necessary security properties, particularly second preimage resistance.

---

# Finding a Collision in a Truncated MD5 Hash Function

Consider the following simplified hash function:

```python
import hashlib

def H(x):
    md5 = hashlib.md5(x).digest()
    return md5[:2]  # Keep only the first 2 bytes of the MD5 hash
```

The standard MD5 hash produces a 16-byte output. However, this function only retains **2 bytes**, resulting in a hash with significantly reduced collision resistance.

We will write a Python script that finds a collision for this simplified hash function. In other words, we will find two distinct inputs \(x\) and \(x'\) such that:

\[
H(x) = H(x'), \quad \text{where} \quad x \neq x'
\]

---

Let's analyse our way of thought: Due to the **birthday paradox**, the collision is relatively easy to find because retaining only **2 bytes** (16 bits) allows only \(2^{16} = 65,536\) possible unique hash values. Hence, finding a collision is feasible by checking around a few hundred randomly or sequentially generated inputs.

Below is a Python script that solves the above test: 

```python
import hashlib

# Define our truncated MD5 hash function
def H(x):
    md5 = hashlib.md5(x).digest()
    return md5[:2]

# Dictionary to store previously seen hashes
hashes_seen = {}

# Iteratively search for a collision
i = 0
while True:
    candidate = f'input_{i}'.encode()
    current_hash = H(candidate)

    if current_hash in hashes_seen:
        # Collision found!
        previous_input = hashes_seen[current_hash]
        print('Collision Found!')
        print(f'Hash (2 bytes): {current_hash.hex()}')
        print(f'Input 1: {previous_input}')
        print(f'Input 2: {candidate}')
        break

    # Record this hash and input for future collision checking
    hashes_seen[current_hash] = candidate
    i += 1

# assert H(b'input_105') == H( b'input_323')  ### it passes 


```

- The script defines the simplified hash function (`H(x)`), taking the first 2 bytes from the MD5 hash of the input.
- It iteratively generates inputs (`input_0`, `input_1`, `input_2`, ...) and calculates their truncated MD5 hash.
- It stores each hash encountered along with its corresponding input in a dictionary.
- Once the script finds a duplicate hash (a collision), it outputs both inputs producing the same hash.

Due to the reduced hash length, this script will typically find a collision *quickly*. 

# Conclusion
This primer introduced the core concepts and properties of hash functions through formal definitions and practical experiments. We examined both well-constructed and insecure examples to highlight what makes a hash function suitable for cryptographic use.

What we’ve seen is only the beginning—there is much more to uncover in the fascinating world of hashing and its role in security, integrity, and computation.

