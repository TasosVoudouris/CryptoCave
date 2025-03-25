# Basic stuff about Python/Sagemath (Cheat sheet)
Before diving deep into the fascinating world of cryptography, we'll begin by building a solid foundation in basic programming skills. We'll start with some essential Python commands—tools that will accompany us throughout our cryptographic journey. Later on, as we encounter more advanced concepts, we’ll also introduce SageMath to handle more complex mathematical operations with ease.

Think of this as your personal Python Cheatsheet—a quick reference guide that you can revisit anytime until these commands become second nature. Don’t worry if you don’t remember everything at once; learning is a gradual process, and this guide is here to support you every step of the way.


## Table of Contents  

- [Strings & byte strings](#strings--byte-strings)
- [Understanding `[0]` in Indexing](##Understanding-`[0]`-in-Indexing)
- [String concatenation](#string-concatenation)
- [Lists / Dictionaries](#lists--dictionaries)
- [List Comprehension](#list-comprehension)
- [File Read/Write](#file-readwrite)
- [ASCII <==> Unicode (ord() & chr())](#ascii--unicode-ord--chr)
- [Hexadecimal <==> Decimal (0x & hex())](#hexadecimal--decimal-0x--hex)
- [Integer ==> Bytes (bytes([...]))](#integer--bytes-bytes)
- [Hexadecimal <==> Bytes (bytes.fromhex() & hex())](#hexadecimal--bytes-bytesfromhex--hex)
- [bytes_to_long() & long_to_bytes()](#bytes_to_long--long_to_bytes)



## Strings & byte strings  

Before diving into Python programming, it is essential to understand how to print output to the console. This allows you to see the results of your code execution. In Python, we use the `print()` function for this purpose.

```python
### BASIC PRINT STATEMENTS ###
print("Hello, World!")  # Prints: Hello, World!
number = 42
print("The number is:", number)  # Prints: The answer is: 42
#############################
```

Python also has different data types that represent various kinds of objects. Some of the most fundamental data types include:

- `str` (string): Represents a sequence of characters, e.g., `'hello'`.
- `int` (integer): Represents whole numbers, e.g., `42`.
- `float`: Represents decimal numbers, e.g., `3.14`.
- `bytes`: Represents sequences of bytes, e.g., `b'hello'`.

Understanding these basic data types will help in writing efficient and error-free code.

Our next trick is how to determine the class of an object in Python. One useful approach is to print the object's type using the `type()` function. This allows us to inspect the data type of any given input, as shown below:

```python
### CHECKING OBJECT TYPES ###
print(type('crypto'))       # <class 'str'> 
print(type(b'crypto'))      # <class 'bytes'> 
print(type('crypto'[0]))    # <class 'str'> 
print(type(b'crypto'[0]))   # <class 'int'> 
print('crypto'[0])          # c 
print(b'crypto'[0])         # 99 
# notice that 99 is the ASCII value of the character 'c' 
############################### 
```

### Understanding `[0]` in Indexing

The `[0]` in the examples above is used for **indexing**, which allows us to access the first element of a sequence. Let's analyze its behavior:

#### **String Indexing (`str`)**

- `'crypto'[0]` extracts the first character of the string `'crypto'`, which is `'c'`.
- The result is still a string (`<class 'str'>`), meaning Python treats individual characters in a string as smaller strings.

#### **Byte String Indexing (`bytes`)**

- `b'crypto'[0]` extracts the first byte of the byte string `b'crypto'`.
- Since `b'crypto'` is a sequence of bytes, indexing does not return a byte object but rather an **integer representing the ASCII value** of the character `'c'`.
- The ASCII value of `'c'` is **99**, which is why `b'crypto'[0]` returns `99` and its type is `<class 'int'>`.

#### **Key Differences**
| Operation         | Output  | Type       |
|------------------|---------|-----------|
| `'crypto'[0]`    | `'c'`   | `<class 'str'>` |
| `b'crypto'[0]`   | `99`    | `<class 'int'>` |

This distinction is important in areas like cryptography, where byte-level operations are crucial, and understanding the difference between `str` and `bytes` ensures correct data manipulation.

We mentioned above *integer representing the ASCII value*, but because here we do not take anything for granted below is the full ASCII table: 

### Complete ASCII Table (0-127)

| Dec | Hex  | Bin         | Char | Dec | Hex  | Bin         | Char | Dec | Hex  | Bin         | Char | Dec | Hex  | Bin         | Char |
|-----|------|------------|------|-----|------|------------|------|-----|------|------------|------|-----|------|------------|------|
| 0   | 0x00 | 00000000   | NUL  | 32  | 0x20 | 00100000   | Space | 64  | 0x40 | 01000000   | @    | 96  | 0x60 | 01100000   | `    |
| 1   | 0x01 | 00000001   | SOH  | 33  | 0x21 | 00100001   | !     | 65  | 0x41 | 01000001   | A    | 97  | 0x61 | 01100001   | a    |
| 2   | 0x02 | 00000010   | STX  | 34  | 0x22 | 00100010   | \"    | 66  | 0x42 | 01000010   | B    | 98  | 0x62 | 01100010   | b    |
| 3   | 0x03 | 00000011   | ETX  | 35  | 0x23 | 00100011   | #     | 67  | 0x43 | 01000011   | C    | 99  | 0x63 | 01100011   | c    |
| 4   | 0x04 | 00000100   | EOT  | 36  | 0x24 | 00100100   | $     | 68  | 0x44 | 01000100   | D    | 100 | 0x64 | 01100100   | d    |
| 5   | 0x05 | 00000101   | ENQ  | 37  | 0x25 | 00100101   | %     | 69  | 0x45 | 01000101   | E    | 101 | 0x65 | 01100101   | e    |
| 6   | 0x06 | 00000110   | ACK  | 38  | 0x26 | 00100110   | &     | 70  | 0x46 | 01000110   | F    | 102 | 0x66 | 01100110   | f    |
| 7   | 0x07 | 00000111   | BEL  | 39  | 0x27 | 00100111   | '     | 71  | 0x47 | 01000111   | G    | 103 | 0x67 | 01100111   | g    |
| 8   | 0x08 | 00001000   | BS   | 40  | 0x28 | 00101000   | (     | 72  | 0x48 | 01001000   | H    | 104 | 0x68 | 01101000   | h    |
| 9   | 0x09 | 00001001   | TAB  | 41  | 0x29 | 00101001   | )     | 73  | 0x49 | 01001001   | I    | 105 | 0x69 | 01101001   | i    |
| 10  | 0x0A | 00001010   | LF   | 42  | 0x2A | 00101010   | *     | 74  | 0x4A | 01001010   | J    | 106 | 0x6A | 01101010   | j    |
| 11  | 0x0B | 00001011   | VT   | 43  | 0x2B | 00101011   | +     | 75  | 0x4B | 01001011   | K    | 107 | 0x6B | 01101011   | k    |
| 12  | 0x0C | 00001100   | FF   | 44  | 0x2C | 00101100   | ,     | 76  | 0x4C | 01001100   | L    | 108 | 0x6C | 01101100   | l    |
| 13  | 0x0D | 00001101   | CR   | 45  | 0x2D | 00101101   | -     | 77  | 0x4D | 01001101   | M    | 109 | 0x6D | 01101101   | m    |
| 14  | 0x0E | 00001110   | SO   | 46  | 0x2E | 00101110   | .     | 78  | 0x4E | 01001110   | N    | 110 | 0x6E | 01101110   | n    |
| 15  | 0x0F | 00001111   | SI   | 47  | 0x2F | 00101111   | /     | 79  | 0x4F | 01001111   | O    | 111 | 0x6F | 01101111   | o    |
| 16  | 0x10 | 00010000   | DLE  | 48  | 0x30 | 00110000   | 0     | 80  | 0x50 | 01010000   | P    | 112 | 0x70 | 01110000   | p    |
| 17  | 0x11 | 00010001   | DC1  | 49  | 0x31 | 00110001   | 1     | 81  | 0x51 | 01010001   | Q    | 113 | 0x71 | 01110001   | q    |
| 18  | 0x12 | 00010010   | DC2  | 50  | 0x32 | 00110010   | 2     | 82  | 0x52 | 01010010   | R    | 114 | 0x72 | 01110010   | r    |
| 19  | 0x13 | 00010011   | DC3  | 51  | 0x33 | 00110011   | 3     | 83  | 0x53 | 01010011   | S    | 115 | 0x73 | 01110011   | s    |
| 20  | 0x14 | 00010100   | DC4  | 52  | 0x34 | 00110100   | 4     | 84  | 0x54 | 01010100   | T    | 116 | 0x74 | 01110100   | t    |

...

| 126 | 0x7E | 01111110   | ~    | 127 | 0x7F | 01111111   | DEL  |


## Working with ASCII, Hexadecimal, and Bytes in Python

Following our discussion on the ASCII table, it's important to understand how to manipulate different data types in Python. These operations are essential when working with text encoding, cryptographic applications, and binary data. Below are some useful commands to **convert between different types** in Python, ensuring smooth operations between various object types.

---

## ASCII <==> Unicode (ord() & chr())  

ASCII and Unicode are fundamental for representing text in programming. Python provides two built-in functions:
- `ord(char)`: Converts a character into its ASCII (or Unicode) integer representation.
- `chr(int)`: Converts an integer back into a character.

```python
### ord() & chr() (ASCII <--> UNICODE)  ###
print(ord('A'))               # 65 (ASCII value of 'A')
print(chr(65))                # 'A' (Character represented by ASCII 65)
########################################### 
```

This is useful when working with text-based operations, encoding, and cryptographic algorithms.

---

## Hexadecimal <==> Decimal (0x & hex())  

Hexadecimal notation is commonly used in computing, particularly in low-level programming and cryptography. Python allows conversion between decimal and hexadecimal representations:

```python
### 0x NOTATION & hex() ###
print(hex(2569))              # '0xa09' (Decimal 2569 converted to Hexadecimal)
###################################################### 
```

- The `hex()` function converts a decimal number to its hexadecimal form.
- The `0x` prefix in Python represents hexadecimal notation.

---

## Integer ==> Bytes (bytes([...]))  

When working with binary data, sometimes we need to convert integers into byte representations. The `bytes()` function helps achieve this:

```python
### bytes([...]) ###
b = bytes([250]) 
print(b)                      # b'\xfa' (Byte representation of integer 250)
############################################### 
```

This is particularly useful when dealing with **binary files, network protocols, or cryptographic applications.**

---

## Hexadecimal <==> Bytes (bytes.fromhex() & hex())  

Hexadecimal encoding is widely used for representing binary data in a human-readable format. Python provides:
- `bytes.fromhex(hex_string)`: Converts a hex string to bytes.
- `.hex()`: Converts bytes into a hex string.

```python
### bytes.fromhex() & .hex() ###
b = bytes.fromhex('414243443031323334') 
print(b)                      # b'ABCD01234' (Hex to bytes conversion)
######################################################### 
```

This is helpful when working with cryptographic keys, file encodings, and networking protocols.

---

## bytes_to_long() & long_to_bytes()  

In cryptographic applications, large numbers are often represented as byte sequences. The `Crypto.Util.number` module provides methods for conversion:

```python
### bytes_to_long() & long_to_bytes() ###
from Crypto.Util.number import long_to_bytes, bytes_to_long 

b = bytes_to_long(b'Hello!') 
print(b)                      # 79600447942433 (Byte string converted to long integer)

original_bytes = long_to_bytes(79600447942433) 
print(original_bytes)         # b'Hello!' (Restores original byte string)
######################################### 
```

These conversions are critical in **cryptography, digital signatures, and blockchain applications.**

---

By mastering these conversion functions, you will be better equipped to handle different data representations in Python, whether for cryptographic protocols, networking, or working with raw binary data. 🚀


## How Can We Transmit the "Backspace" Character?

The **Backspace** character (`ASCII 8`) is a **non-printable** control character, meaning it does not display any visual representation when printed. However, if we need to transmit it (e.g., in a network message, file, or a string), we can represent it in various ways in Python.

### Solution:

We can use:
1. **Escape sequence**: `"\b"`
2. **chr() function**: `chr(8)`
3. **Raw bytes**: `b'\x08'`

#### Example in Python:

```python
# Using the escape sequence
print("Hello\bWorld")  # The '\b' will act as a backspace

# Using chr() to represent ASCII 8
backspace_char = chr(8)
print(f"Backspace character: {repr(backspace_char)}")  # Displays the representation

# Using raw bytes
backspace_bytes = b'\x08'
print(f"Backspace in bytes: {backspace_bytes}")
```

### Explanation:
- `"\b"` moves the cursor **one step back**, so `"Hello\bWorld"` prints `"HellWorld"`.
- `chr(8)` gives us the backspace character as a **string**.
- `b'\x08'` represents the backspace character in **byte form**.

These methods ensure we can correctly encode and transmit the **Backspace** character when necessary.

---

## Lists / Dictionaries  

### What is a List?
A **list** in Python is an ordered, mutable collection that can store multiple values, including different data types. Lists are one of the most commonly used data structures because they allow easy modification and indexing.

#### **List Operations & Examples**
```python
### LISTS ###
l = [9, 5, 2, 13, 7] 
print(l[0])                   # 9  (First element)
print(l[-1])                  # 7  (Last element)
print(l[3:])                  # [13, 7]  (Slice from index 3 to end)
print(l[:-2])                 # [9, 5, 2]  (All except last two elements)

l1 = [6, 6, 6, 6, 6, 6, 6] 
l2 = [6] * 7  # Creates a list with seven elements all set to 6
print(l1 == l2)               # True (Both lists contain the same values)
```

### What is a Dictionary?
A **dictionary** in Python is an unordered collection of key-value pairs. Unlike lists, where elements are accessed by index, dictionary elements are accessed using keys, making retrieval operations fast and intuitive.

#### **Dictionary Operations & Examples**
```python
### DICTIONARIES ###
d = { 'a': 97, 'b': 98, 'c': 99, 'd': 100 }
print(d['c'])                 # 99  (Retrieves value associated with key 'c')
```

### Key Differences Between Lists & Dictionaries
| Feature        | List                        | Dictionary                   |
|---------------|----------------------------|------------------------------|
| Ordered?      | Yes                         | Python 3.7+ (insertion order) |
| Mutable?      | Yes                         | Yes                          |
| Indexed By?   | Integer index               | Keys                         |
| Duplicate Elements? | Yes                   | No (keys must be unique)     |

---

## List Comprehension  

**List comprehension** provides a concise way to create lists. Instead of using loops, we can generate lists in a single line of code, making it more readable and efficient.

#### **List Comprehension Example**
```python
### LIST COMPREHENSION ###
nums = [1, 3, 5, 7, 9, 11] 
newlist = [i**3 for i in nums] 
print('With list comprehension:', newlist) 
# Output: [1, 27, 125, 343, 729, 1331]
```

### **Breaking Down the Syntax**
```python
[i**3 for i in nums]
```
- `i**3`: The expression that defines what each element in the new list will be.
- `for i in nums`: The loop that iterates over `nums`.
- The result is a new list where each element is the cube of the corresponding element in `nums`.

### **Why Use List Comprehension?**
✅ More concise and readable than loops.

✅ Often faster than traditional loops.

✅ Reduces unnecessary variable assignments.

## Lists and the zip() Function  

Lists are one of the most versatile and commonly used data structures in Python. The `zip()` function is particularly useful when working with multiple lists.

### Using `zip()` to Combine Lists

The `zip()` function allows us to pair elements from multiple lists, creating tuples of corresponding elements.

```python
### zip() ###
a1 = ['a', 'b', 'c', 'd'] 
a2 = [13, 17, 20, 26] 
print(list(zip(a1, a2)))       # [('a', 13), ('b', 17), ('c', 20), ('d', 26)] 
############# 
```

### Explanation:
- The `zip(a1, a2)` function pairs corresponding elements from `a1` and `a2`.
- The result is a **list of tuples**, where each tuple contains one element from each list.
- If the lists are of **unequal length**, `zip()` stops at the shortest list.

### Practical Use Cases:
✅ Useful in iterating over multiple lists simultaneously.

✅ Helps in mapping related data efficiently.

✅ Can be used to **transpose matrices** in numerical computations.

---


## String Concatenation  

String concatenation allows us to join multiple strings or byte strings together. In Python, we can concatenate strings using the `+` operator.

#### **(Byte) String Concatenation Example**
```python
### (BYTE) STRING CONCATENATION ###
string = b'This' + b'message' + b'is' + b'concatenated' 
print('String result:', string) 

byte_string = b'Concatenate' + b'byte' + b'strings' 
print('Byte string result:', byte_string) 
################################### 
```

### **Key Differences Between Strings and Byte Strings**
| Feature        | String (`str`)               | Byte String (`bytes`)      |
|---------------|-----------------------------|---------------------------|
| Representation | Unicode characters          | Raw bytes                 |
| Concatenation | `+` operator                 | `+` operator              |
| Indexing      | Returns `str`                | Returns `int` (ASCII value) |
| Example       | `'Hello' + 'World'` → `'HelloWorld'` | `b'Hello' + b'World'` → `b'HelloWorld'` |



## File Read/Write  

Before diving into cryptographic operations, it's essential to learn how to read and write files, as encryption and decryption often involve handling files.

Python provides a simple way to handle files using the `open()` function. Below are examples of writing and reading a file:

```python
### FILE READ/WRITE ###
# Writing to a file
with open('write_me', 'w') as f: 
  f.write('Hello!') 

# Reading from a file
with open('write_me', 'r') as f: 
  print(f.read())             # Output: Hello! 
####################### 
```

### Explanation:
- `'w'` mode opens the file for writing. If the file does not exist, it creates one.
- `'r'` mode opens the file for reading.
- The `with open(...) as f:` syntax ensures the file is properly closed after reading or writing, preventing data corruption or memory leaks.

Understanding file operations is crucial when working with encrypted data, as storing and retrieving encrypted messages securely is an essential part of cryptographic workflows.










