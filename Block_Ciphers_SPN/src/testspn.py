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