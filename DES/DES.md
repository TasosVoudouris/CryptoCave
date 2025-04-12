# Data Encryption Standard (DES)

# Table of Contents

- [Data Encryption Standard (DES)](#data-encryption-standard-des)
- [Table of Contents](#table-of-contents)
  - [Key Concepts of DES](#key-concepts-of-des)
  - [Preprocessing Functions](#preprocessing-functions)
  - [Construction of Permutation-Box (P-BOX)](#construction-of-permutation-box-p-box)
    - [Expansion P-Box: 32-bit to 48-bit Transformation](#expansion-p-box-32-bit-to-48-bit-transformation)
    - [Straight P-Box: Simple Reordering](#straight-p-box-simple-reordering)
    - [Compression P-Box: 4-bit to 3-bit Mapping (with Overlap)](#compression-p-box-4-bit-to-3-bit-mapping-with-overlap)
  - [S-Box: Substitution in DES](#s-box-substitution-in-des)
    - [Row and Column Extraction](#row-and-column-extraction)
    - [DES S-Boxes](#des-s-boxes)
    - [Internals of Row-Column Mapping](#internals-of-row-column-mapping)
    - [Building S-Boxes from Matrices](#building-s-boxes-from-matrices)
    - [Swapper](#swapper)
  - [Mixer](#mixer)
    - [Mixer Transformation](#mixer-transformation)
  - [Feistel Round](#feistel-round)
    - [Feistel Round example](#feistel-round-example)
  - [Wholesome DES and final testing](#wholesome-des-and-final-testing)
    - [The `DES` class](#the-des-class)
- [WRAP-UP](#wrap-up)
    - [DES Components We Built](#des-components-we-built)


The Data Encryption Standard (DES) is one of the earliest and most influential symmetric-key algorithms developed for the encryption of digital information. While DES is no longer considered secure for modern applications due to its 56-bit key size, it remains a foundational concept in cryptography and is often used for educational purposes. For more details and nice images you can always visit [DES supplementary material – Wikipedia](https://en.wikipedia.org/wiki/DES_supplementary_material).


## Key Concepts of DES
- DES is a block cipher that encrypts 64-bit blocks of plaintext using a 56-bit secret key.

- The algorithm involves 16 rounds of Feistel-style transformations.

- In each round:

    - The input is split into left and right halves.
    - A function is applied to the right half, combined with the round key, and the result is XORed with the left half.
    - The two halves are then swapped (except for the final round). 
    - Round keys of 48 bits are derived from the original 64-bit key and used in each round.

## Preprocessing Functions

To implement DES, we begin by defining a set of utility functions. These help with common tasks like binary conversion, character encoding, and bit manipulation. These are particularly important since DES operates on binary representations of data.


```python
############# Converts an integer into its binary representation as a string of fixed length.
def int_to_bin(number: int, block_size=8) -> str:
    binary = bin(number)[2:]
    return '0' * (block_size - len(binary)) + binary
 ########## This ensures that all binary values are consistently padded to the same block size


############## Converts a lowercase alphabetic character to a number from 0 to 25.
def char_2_num(letter: str) -> int:
    return ord(letter) - ord('a')

########### Inverse of char_2_num. Converts a number (0–25) back to a lowercase character.
def num_2_char(number: int) -> str:
    return chr(ord('a') + number)

############## Basic modulo operation. Used for cyclic indexing or arithmetic operations within a bounded domain.
############## More about this when we will enter the mathematical cave! Hold tight!
def mod(a, b):
    return a % b

################# Performs a left circular shift (also known as rotate-left) on a binary string.
################ This operation is crucial in the DES key schedule for generating new subkeys from the original key.
def left_circ_shift(binary: str, shift: int) -> str:
    shift = shift % len(binary)
    return binary[shift:] + binary[0: shift]
```
These foundational functions prepare the way for more complex components of DES, such as the Feistel function, key scheduling, and permutation operations, which we will explore next.

## Construction of Permutation-Box (P-BOX) 
We now define a Permutation Box (P-Box), a component heavily used in the DES algorithm. P-Boxes perform bit-level permutations and are essential for introducing diffusion in the cipher. In DES, we encounter three main types of P-Boxes:

1. Straight P-Box — used after substitution to rearrange bits.

2. Expansion P-Box — expands a 32-bit half-block to 48 bits for key mixing.

3. Compression P-Box — compresses the 56-bit shifted key into a 48-bit round key.

The `PBox` class defines a `permutate()` method, which takes a binary sequence (represented as a list or string) and returns its permuted version according to the P-Box mapping.

In addition to this method, several static methods are included to define the **standard DES permutation tables**, such as the initial permutation, final permutation, key scheduling permutations, and round expansions.

These components form the backbone of DES’s bit-level transformation logic. Below they are implemented in Python: 


```python
class PBox:
    def __init__(self, key: dict):
        self.key = key
        self.in_degree = len(key)
        self.out_degree = sum(len(value) if isinstance(value, list) else 1 for value in key.values())

    def __repr__(self) -> str:
        return 'PBox' + str(self.key)

    def permutate(self, sequence: list) -> str:
        result = [0] * self.out_degree
        for index, value in enumerate(sequence):
            if (index + 1) in self.key:
                indices = self.key.get(index + 1, [])
                indices = indices if isinstance(indices, list) else [indices]
                for i in indices:
                    result[i - 1] = value
        return ''.join(map(str, result))

    def is_invertible(self) -> bool:
        return self.in_degree == self.out_degree

    def invert(self):
        if self.is_invertible():
            result = {}
            for index, mapping in self.key.items():
                result[mapping] = index
            return PBox(result)

    @staticmethod
    def identity(block_size=64):
        return PBox({index: index for index in range(1, block_size + 1)})

    @staticmethod
    def from_list(permutation: list):
        mapping = {}
        for index, value in enumerate(permutation):
            indices = mapping.get(value, [])
            indices.append(index + 1)
            mapping[value] = indices
        return PBox(mapping)

    @staticmethod
    def des_initial_permutation():
        return PBox.from_list(
            [58, 50, 42, 34, 26, 18, 10, 2,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 1,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7]
        )

    @staticmethod
    def des_final_permutation():
        return PBox.from_list(
            [40, 8, 48, 16, 56, 24, 64, 32,
             39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25]
        )

    @staticmethod
    def des_single_round_expansion():
        """This is the Permutation made on the right half of the block to convert 32 bit --> 48 bits in DES Mixer"""
        return PBox.from_list(
            [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]
        )

    @staticmethod
    def des_single_round_final():
        """This is the permutation made after the substitution happens in each round"""
        return PBox.from_list(
            [16, 7, 20, 21, 29, 12, 28, 17,
             1, 15, 23, 26, 5, 18, 31, 10,
             2, 8, 24, 14, 32, 27, 3, 9,
             19, 13, 30, 6, 22, 11, 4, 25]
        )

    @staticmethod
    def des_key_initial_permutation():
        return PBox.from_list(
            [57, 49, 41, 33, 25, 17, 9,
             1, 58, 50, 42, 34, 26, 18,
             10, 2, 59, 51, 43, 35, 27,
             19, 11, 3, 60, 52, 44, 36,
             63, 55, 47, 39, 31, 23, 15,
             7, 62, 54, 46, 38, 30, 22,
             14, 6, 61, 53, 45, 37, 29,
             21, 13, 5, 28, 20, 12, 4]
        )

    @staticmethod
    def des_shifted_key_permutation():
        """PC2 Matrix for compression PBox 56 bit --> 48 bit"""
        return PBox.from_list(
            [14, 17, 11, 24, 1, 5, 3, 28,
             15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]
        )
```

Now that we have defined the PBox class, let's explore how we can use it to model real DES transformations using various types of Permutation Boxes.

### Expansion P-Box: 32-bit to 48-bit Transformation

In DES, before mixing with the round key, the right half of the block (which is 32 bits) is expanded to 48 bits using an Expansion P-Box. This step allows for mixing with the 48-bit round key.

```python
# Create the DES expansion box (32 bits to 48 bits)
expansion_p_box = PBox.des_single_round_expansion()

# Apply the permutation to a 32-bit number (converted to binary string)
permutation = expansion_p_box.permutate(int_to_bin(1234, block_size=32))

print('Permutation:', permutation)
print('Output Length:', len(permutation))
```
We have as an output: `Permutation: 000000000000000000000000000000001001011010100100 , Output Length: 48`. Here, `int_to_bin(1234, block_size=32)` converts the integer into a 32-bit binary string. The `permutate()` method then expands it to 48 bits according to the standard expansion table.

### Straight P-Box: Simple Reordering

You can also define custom P-Boxes using a list. The following example reorders characters in a string according to the given mapping:

```python
# Create a straight P-Box that reorders a string
straight_p_box = PBox.from_list([4, 1, 3, 2])
p = straight_p_box.permutate('help')
print(p) #phle
```
The list `[4, 1, 3, 2]` means:

- Character 1 → position 4

- Character 2 → position 1

- Character 3 → position 3

- Character 4 → position 2

Thus, `"help"` is transformed into `"phle"`.

### Compression P-Box: 4-bit to 3-bit Mapping (with Overlap)

The following example simulates a Compression P-Box, commonly used to reduce 56-bit keys to 48 bits in DES key scheduling:

```python
# Create a compression P-Box
compression_box = PBox.from_list([3, 3, 2, 1])
p = compression_box.permutate('love')
print(p) # vvol
```
The compression logic here maps:

- Input 1 → position 3

- Input 2 → position 3 (overwriting previous)

- Input 3 → position 2

- Input 4 → position 1

This demonstrates how a compression P-Box can collapse multiple input bits into fewer output positions (and overwrite earlier mappings), which is part of how key reduction works in DES. The whole `PBox` class is presented below:

```python
############################### FULL P-BOX CLASS ##########################
class PBox:
    def __init__(self, key: dict):
        self.key = key
        self.in_degree = len(key)
        self.out_degree = sum(len(value) if isinstance(value, list) else 1 for value in key.values())

    def __repr__(self) -> str:
        return 'PBox' + str(self.key)

    def permutate(self, sequence: list) -> str:
        result = [0] * self.out_degree
        for index, value in enumerate(sequence):
            if (index + 1) in self.key:
                indices = self.key.get(index + 1, [])
                indices = indices if isinstance(indices, list) else [indices]
                for i in indices:
                    result[i - 1] = value
        return ''.join(map(str, result))

    def is_invertible(self) -> bool:
        return self.in_degree == self.out_degree

    def invert(self):
        if self.is_invertible():
            result = {}
            for index, mapping in self.key.items():
                result[mapping] = index
            return PBox(result)

    @staticmethod
    def identity(block_size=64):
        return PBox({index: index for index in range(1, block_size + 1)})

    @staticmethod
    def from_list(permutation: list):
        mapping = {}
        for index, value in enumerate(permutation):
            indices = mapping.get(value, [])
            indices.append(index + 1)
            mapping[value] = indices
        return PBox(mapping)

    @staticmethod
    def des_initial_permutation():
        return PBox.from_list(
            [58, 50, 42, 34, 26, 18, 10, 2,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 1,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7]
        )

    @staticmethod
    def des_final_permutation():
        return PBox.from_list(
            [40, 8, 48, 16, 56, 24, 64, 32,
             39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25]
        )

    @staticmethod
    def des_single_round_expansion():
        """This is the Permutation made on the right half of the block to convert 32 bit --> 48 bits in DES Mixer"""
        return PBox.from_list(
            [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]
        )

    @staticmethod
    def des_single_round_final():
        """This is the permutation made after the substitution happens in each round"""
        return PBox.from_list(
            [16, 7, 20, 21, 29, 12, 28, 17,
             1, 15, 23, 26, 5, 18, 31, 10,
             2, 8, 24, 14, 32, 27, 3, 9,
             19, 13, 30, 6, 22, 11, 4, 25]
        )

    @staticmethod
    def des_key_initial_permutation():
        return PBox.from_list(
            [57, 49, 41, 33, 25, 17, 9,
             1, 58, 50, 42, 34, 26, 18,
             10, 2, 59, 51, 43, 35, 27,
             19, 11, 3, 60, 52, 44, 36,
             63, 55, 47, 39, 31, 23, 15,
             7, 62, 54, 46, 38, 30, 22,
             14, 6, 61, 53, 45, 37, 29,
             21, 13, 5, 28, 20, 12, 4]
        )

    @staticmethod
    def des_shifted_key_permutation():
        """PC2 Matrix for compression PBox 56 bit --> 48 bit"""
        return PBox.from_list(
            [14, 17, 11, 24, 1, 5, 3, 28,
             15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]
        )
```



## S-Box: Substitution in DES

In the Data Encryption Standard (DES), S-Boxes (Substitution Boxes) are critical components responsible for introducing confusion — one of the two core principles of a secure block cipher (the other being diffusion).

Each S-Box maps a 6-bit input into a 4-bit output by consulting a pre-defined lookup table.

An S-Box:

- Takes a 6-bit binary input

- Extracts the row and column using a special rule

- Looks up the output in a 4-row, 16-column table

- Returns a 4-bit output (in binary)

### Row and Column Extraction

For a 6-bit binary string `b = b₀b₁b₂b₃b₄b₅`:

- Row is formed using the first and last bits: `b₀b₅`

- Column is formed using the middle four bits: `b₁b₂b₃b₄`

So for example, '000100' becomes:

- Row: `00 → 0`

- Column: `0010 → 2`

So we define a `Sbox` class which contains:

- A lookup table

- A method to extract row and column from a 6-bit input

- Callable interface `(__call__)` to perform substitution

```python
class SBox:
    def __init__(self, table: dict, block_size=4, func=lambda binary: (binary[0] + binary[5], binary[1:5])):
        self.table = table
        self.block_size = block_size
        self.func = func

    def __call__(self, binary: str) -> str:
        a, b = self.func(binary)
        a, b = int(a, base=2), int(b, base=2)
        if (a, b) in self.table:
            return int_to_bin(self.table[(a, b)], block_size=self.block_size)
        else:
            return binary
```
Let’s test a manually created S-Box that maps 2-bit inputs using a basic lookup rule:

```python
s_box = SBox(block_size=2, table={
    (0, 0): 5,
    (0, 1): 6,
    (1, 0): 8,
    (1, 1): 7
}, func=lambda x: (x[0], x[1]))

print(s_box('00'))  # '101'
print(s_box('01'))  # '110'
print(s_box('10'))  # '1000'
print(s_box('11'))  # '111'
```
Each pair (row, col) maps to a specific integer which is then returned as a binary string.

### DES S-Boxes

The DES algorithm uses eight predefined S-Boxes. Each takes a 6-bit input and returns a 4-bit output. These are defined using `@staticmethods` such as `SBox.des_s_box1(), SBox.des_s_box2(), ..., SBox.des_s_box8()`.

Each table consists of a 4x16 matrix. You can retrieve all eight like this: `sboxes = SBox.des_single_round_substitutions()`.  
Or just the first one:

```python
s_box2 = SBox.des_s_box1()
binary = '000100'
print(s_box2(binary))  # Example output: '1101'
```
### Internals of Row-Column Mapping
This function is what DES uses to extract row and column from a 6-bit binary string:

```python
@staticmethod
def des_confusion(binary: str) -> tuple:
    return binary[0] + binary[5], binary[1: 5]
```
That’s:

- `binary[0] + binary[5]`: first and last bits → row

- `binary[1:5]`: middle four bits → column

### Building S-Boxes from Matrices

You can define your own S-Box using a list of lists (a 4x16 grid):
```python
@staticmethod
def from_list(sequence: list):
    mapping = {}
    for row in range(len(sequence)):
        for column in range(len(sequence[0])):
            mapping[(row, column)] = sequence[row][column]
    return SBox(table=mapping)
```
This provides a general-purpose interface for defining substitution tables, not just for DES but for any substitution-based block cipher.


The full `Sbox` class is below: 

```python

################### FULL S-BOX CLASS  ##################
class SBox:
    def __init__(self, table: dict, block_size=4, func=lambda binary: (binary[0] + binary[5], binary[1:5])):
        self.table = table
        self.block_size = block_size
        self.func = func

    def __call__(self, binary: str) -> str:
        a, b = self.func(binary)
        a, b = int(a, base=2), int(b, base=2)
        if (a, b) in self.table:
            return int_to_bin(self.table[(a, b)], block_size=self.block_size)
        else:
            return binary

    @staticmethod
    def des_single_round_substitutions():
        return [SBox.forDESSubstitution(block) for block in range(1, 9)]

    @staticmethod
    def identity():
        return SBox(func=lambda binary: ('0', '0'), table={})

    @staticmethod
    def forDESSubstitution(block):
        if block == 1: return SBox.des_s_box1()
        if block == 2: return SBox.des_s_box2()
        if block == 3: return SBox.des_s_box3()
        if block == 4: return SBox.des_s_box4()
        if block == 5: return SBox.des_s_box5()
        if block == 6: return SBox.des_s_box6()
        if block == 7: return SBox.des_s_box7()
        if block == 8: return SBox.des_s_box8()

    @staticmethod
    def des_confusion(binary: str) -> tuple:
        """"Takes a 6-bit binary string as input and returns a 4-bit binary string as output"""
        return binary[0] + binary[5], binary[1: 5]

    @staticmethod
    def from_list(sequence: list):
        mapping = {}
        for row in range(len(sequence)):
            for column in range(len(sequence[0])):
                mapping[(row, column)] = sequence[row][column]
        return SBox(table=mapping)

    @staticmethod
    def des_s_box1():
        return SBox.from_list(
            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]
        )

    @staticmethod
    def des_s_box2():
        return SBox.from_list(
            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]
        )

    @staticmethod
    def des_s_box3():
        return SBox.from_list(
            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]
        )

    @staticmethod
    def des_s_box4():
        return SBox.from_list(
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]
        )

    @staticmethod
    def des_s_box5():
        return SBox.from_list(
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]
        )

    @staticmethod
    def des_s_box6():
        return SBox.from_list(
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]
        )

    @staticmethod
    def des_s_box7():
        return SBox.from_list(
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]
        )

    @staticmethod
    def des_s_box8():
        return SBox.from_list(
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
        )
```

### Swapper
In DES, the `Swapper` is used as part of the Feistel structure to alternate the left and right halves of the data block between rounds.

The idea is simple:

- Given a binary string of fixed length (usually 64 bits in DES),

- Split it into two halves: left and right,

- Return them in swapped order.

This operation ensures that each half of the input data gets processed equally by the Feistel rounds. The `Swapper` class implements this functionality using a fixed block size (default is 64 bits).

```python
class Swapper:
    def __init__(self, block_size=64):
        self.block_size = block_size

    def encrypt(self, binary: str) -> str:
        l, r = binary[0: self.block_size // 2], binary[self.block_size // 2:]
        return r + l

    def decrypt(self, binary: str) -> str:
        return self.encrypt(binary)

###################### a simple example with the string '11110000' ##################
swapper = Swapper(block_size=8)
ciphertext = swapper.encrypt('11110000')
print(ciphertext)  # Output: '00001111'
print(swapper.decrypt(ciphertext))  # Output: '11110000'

```
Let’s simulate swapping a 64-bit binary number — just like in a real DES round:

```python
swapper_64_bit = Swapper()
ciphertext = swapper_64_bit.encrypt(int_to_bin(100, block_size=64))
print(ciphertext) # 0000000000000000000000000110010000000000000000000000000000000000
```
Notice that the integer `100` is converted to a 64-bit binary string, then swapped across the middle. And if we want to return to the original `100`: 

```python
original = int(swapper_64_bit.decrypt(ciphertext), base=2)
print(original)  # Output: 100
```
This verifies that our `Swapper` behaves correctly and is involutory (i.e., self-inverse).

Before we proceed, keep in mind the following properties:

- The encryption and decryption functions are identical. Swapping twice restores the original string.

- This is why the Feistel structure is inherently invertible — no need to reverse the round function logic.

## Mixer
In DES, the `Mixer` is the core component of each Feistel round. It applies a non-invertible transformation on the right half of the data block and then combines the result with the left half using a bitwise XOR.

This process ensures that every round introduces confusion and diffusion into the plaintext.

### Mixer Transformation
Given a binary block split into halves $L || R$ we have the following:
```python
L_new = L ⊕ f(R, K)
R_new = R
```
The function $f$ uses a combination of:

- Expansion permutation

- Key mixing

- S-box substitution

- Final permutation

This non-invertible logic ensures security and allows the Feistel structure to maintain overall reversibility.

Below we provide the `Mixer` class that encapsulates all components of the DES round function $f$ :

```python
class Mixer:
    def __init__(self, key: int, func=lambda a, b: a % b, block_size=64,
                 initial_permutation=None, final_permutation=None,
                 substitutions: list = None, substitution_block_size=6):
        self.func = func
        self.block_size = block_size
        self.initial_permutation = PBox.identity(block_size // 2) if initial_permutation is None else initial_permutation
        self.final_permutation = PBox.identity(block_size // 2) if final_permutation is None else final_permutation
        self.substitutions = SBox.des_single_round_substitutions() if substitutions is None else substitutions
        self.substitution_block_size = substitution_block_size
        self.key = key

    def encrypt(self, binary: str) -> str:
        l, r = binary[0: self.block_size // 2], binary[self.block_size // 2:]
        # expansion PBox
        r1: str = self.initial_permutation.permutate(r)

        # applying function
        r2: str = int_to_bin(self.func(int(r1, base=2), self.key), block_size=self.initial_permutation.out_degree)

        # applying the substitution matrices
        r3: str = ''
        for i in range(len(self.substitutions)):
            block: str = r2[i * self.substitution_block_size: (i + 1) * self.substitution_block_size]
            r3 += self.substitutions[i](block)

        # applying final permutation
        r3: str = self.final_permutation.permutate(r3)

        # applying xor
        l = int_to_bin(int(l, base=2) ^ int(r3, base=2), block_size=self.block_size // 2)
        return l + r

    def decrypt(self, binary:str) -> str:
        return self.encrypt(binary)

    @staticmethod
    def des_mixer(key: int):
        return Mixer(
          key=key,
          initial_permutation=PBox.des_single_round_expansion(),
          final_permutation=PBox.des_single_round_final(),
          func=lambda a, b: a % b
        )
```
The parameters used are the following:

- `key`: The round key (48-bit in DES).

- `func`: A binary operation applied to the expanded right-half and key (can be mod, XOR, etc.).

- `block_size`: Default is 64 bits.

- `initial_permutation`: Expansion box (32 → 48 bits).

- `final_permutation`: Straight P-box (applied after S-boxes).

- `substitutions`: A list of 8 DES S-boxes.

- `substitution_block_size`: Each S-box operates on 6-bit input.

This next code block demonstrates how to use the DES-specific Mixer class we just defined to perform one round of encryption and decryption on a 64-bit block, using a small test key and integer input.


```python
# We craete a DES specific mixer. That means that the block_size will be 64 and DES specific PBoxes and SBoxes will be used.
# Also we use the mod function when performing a non-invertible operation over r ad Key hence f = r % Key
mixer = Mixer.des_mixer(key=3)
number = 1001
binary = int_to_bin(number, block_size=64)
print('Plaintext:', binary)

### We convert the integer 1001 to a 64-bit binary string using our utility function int_to_bin(). ######

##### encrypt ############
ciphertext = mixer.encrypt(binary)
print('Ciphertext:', ciphertext)

########### The right half remains untouched (Feistel structure).
# The left half is modified by f(r, key) using the above structures mentioned #############

# decrypting using the Mixer
decrypted = mixer.decrypt(ciphertext)
print('Decrypted:', decrypted)

# printing the integer based output
print(int(decrypted, base=2))
```

## Feistel Round

A single round of the DES algorithm is based on the Feistel structure. In each round, two main components are used in succession:

 - `Mixer` – applies a key-based transformation to the right half of the input and XORs the result with the left half.

- `Swapper` – switches the left and right halves.

During **encryption**, the order is: `Mixer → Swapper`

During **decryption**, the inverse order is used: `Swapper⁻¹ → Mixer⁻¹` (which is just running the same functions in reverse since Feistel is symmetric).

Below is provided as a class: 

```python
class Round:
    def __init__(self, mixer):
        self.mixer = mixer
        self.swapper = NoneSwapper()

    @staticmethod
    def with_swapper(mixer: Mixer):
        temp = Round(mixer)
        temp.swapper = Swapper(block_size=mixer.block_size)
        return temp

    @staticmethod
    def without_swapper(mixer: Mixer):
        return Round(mixer)

    def encrypt(self, binary: str) -> str:
        binary = self.mixer.encrypt(binary)
        return self.swapper.encrypt(binary)

    def decrypt(self, binary: str) -> str:
        binary = self.swapper.decrypt(binary)
        return self.mixer.decrypt(binary)
```
*You can use `without_swapper` in the final round of DES where swapping is not needed.*

### Feistel Round example

Let’s walk through a simple example that demonstrates how the Feistel round works, both with and without a `Swapper`.

```python
################## EXAMPLE WITHOUT SWAPPER ONLY MIXER ###########
number = 12345
binary = int_to_bin(number, block_size=64)
round1 = Round.without_swapper(Mixer.des_mixer(key=17))
ciphertext = round1.encrypt(binary)
print('Ciphertext:', ciphertext) # Ciphertext: 1101000011011000110100111011110000000000000000000011000000111001

### DECRYPT 
print('Decrypted Number:', int(round1.decrypt(ciphertext), base=2)) # 12345


############## EXAMPLE WITH SWAPPER AND MIXER ###############
number = 12345
binary = int_to_bin(number, block_size=64)
round1 = Round.with_swapper(Mixer.des_mixer(key=17))
ciphertext = round1.encrypt(binary)
print('Ciphertext:', ciphertext) # 0000000000000000001100000011100111010000110110001101001110111100

###### DECRYPT
print('Decrypted Number:', int(round1.decrypt(ciphertext), base=2)) # 12345
```

Keep in mind the following:

| Configuration         | Uses Swapper | Ciphertext | Decryption Output (Plaintext) |
|-----------------------|--------------|------------|-------------------------------|
| Feistel Round (Mixer only)    | ❌ No         |  Different   | ✅ Same as original          |
| Feistel Round (Mixer + Swapper) | ✅ Yes        |  Different   | ✅ Same as original          |

*The ciphertext will differ depending on whether the Swapper is used, because it changes the order of the bits after the Mixer step*.


## Wholesome DES and final testing

Now, we put everything together to create a working DES cipher system, built from scratch using our own `PBox, SBox, Mixer, Swapper`, and `Round` classes. Buckle up!

### The `DES` class

We now define the DES class that encapsulates the entire encryption process. The DES cipher uses:

- 64-bit keys (with some parity bits ignored),

- 64-bit blocks of plaintext,

- 16 Feistel rounds, each involving mixing and (optionally) swapping.

Each round:

1. Derives a unique subkey using PC-1 and PC-2 permutations with shifts.

2. Builds a round function using DES-specific Mixer.

3. Optionally adds a Swapper (except for the final round).

```python
class DES:
    def __init__(self, key: int):
        self.key = int_to_bin(key, block_size=64)
        self.PC_1 = PBox.des_key_initial_permutation()
        self.PC_2 = PBox.des_shifted_key_permutation()
        self.single_shift = {1, 2, 9, 16}
        self.rounds = self.generate_rounds()

        def encrypt(self, binary: str) -> str:
        for round in self.rounds:
            binary = round.encrypt(binary)
        return binary

        ################ encryption + decryption  ##########
    def decrypt(self, binary: str) -> str:
        for round in self.rounds[::-1]:
            binary = round.decrypt(binary)
        return binary
    
        def encrypt_message(self, plaintext: str) -> list:
        return [int(self.encrypt(int_to_bin(ord(c), block_size=64)), base=2) for c in plaintext.lower()]

    ################ encryption + decryption of text messages ##########
    def decrypt_message(self, ciphertext_stream: list) -> str:
        return ''.join(map(chr, self.plaintext_stream(ciphertext_stream)))

    def plaintext_stream(self, ciphertext_stream: list) -> list:
        return [int(self.decrypt(int_to_bin(c, block_size=64)), base=2) for c in ciphertext_stream]

    ############# round key generation
    def generate_rounds(self) -> list:
        rounds = []
        self.key = self.PC_1.permutate(self.key)
        l, r = self.key[0:32], self.key[32:]

        for i in range(1, 17):
            shift = 1 if i in self.single_shift else 2
            l, r = left_circ_shift(l, shift), left_circ_shift(r, shift)
            key = int(self.PC_2.permutate(l + r), base=2)

            mixer = Mixer.des_mixer(key)
            cipher = Round.with_swapper(mixer) if i != 16 else Round.without_swapper(mixer)
            rounds.append(cipher)

        return rounds

############### TESTING ##############

number = 1312
binary = int_to_bin(number, block_size=64)

des = DES(key=78)
ciphertext = des.encrypt(binary)
print('Plaintext:', binary)
print('Ciphertext:', ciphertext)

# Decrypting
decrypted = des.decrypt(ciphertext)
print('Decrypted:', decrypted)
print('Value:', int(decrypted, base=2))

############## TEXT MESSAGE EXAMPLE ############# 
message = 'We did it!'
ciphertext = des.encrypt_message(message)
print('Ciphertext:', ciphertext)

# Decryption
decrypted = des.decrypt_message(ciphertext)
print('Decrypted:', decrypted)
```
# WRAP-UP 
In this tutorial, we implemented DES from scratch in Python, focusing on modular design, educational clarity, and cryptographic structure. Here's a summary of what we covered:

### DES Components We Built

| Component   | Type         | Input                          | Output                         | Purpose                                                                 |
|-------------|--------------|--------------------------------|--------------------------------|-------------------------------------------------------------------------|
| `PBox`      | Permutation  | Bit string                     | Bit string (reordered)         | Bit-level permutation used in initial/final perm, expansion, compression |
| `SBox`      | Substitution | 6-bit binary string            | 4-bit binary string            | Non-linear substitution using S-box tables                             |
| `Swapper`   | Swapping     | 64-bit bit string              | 64-bit bit string (halves swapped) | Implements the Feistel swap operation                              |
| `Mixer`     | Core Round   | 64-bit bit string + key        | 64-bit bit string              | Applies Fiestel logic: \( L \gets L \oplus f(R, K) \)                 |
| `Round`     | Feistel Round| 64-bit bit string              | 64-bit bit string              | One round of DES: Mixer + optional Swapper                            |
| `DES`       | Full Cipher  | 64-bit message or full string  | Ciphertext (bit string or list)| Full DES logic: 16 rounds, key scheduling, encryption/decryption       |


I provide in the `src` folder the file `wholesomeDES.py`, now with a few wholesome tweaks:

- Improved print statements so things look a bit cleaner and more readable.

- Changed the line `for index, letter in enumerate(plaintext.lower()):` to `for index, letter in enumerate(plaintext):` — because some of us (👀) might want to encrypt messages with CAPITAL letters and still pass that final assert. You know who you are.

There might be a couple more subtle changes too—go check it out if you're curious. You might uncover a few secrets I tucked in there 😉.
