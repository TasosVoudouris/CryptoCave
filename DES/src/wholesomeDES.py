####################### HELPER FUNCTIONS###################

def int_to_bin(number: int, block_size=8) -> str:
    binary = bin(number)[2:]
    return '0' * (block_size - len(binary)) + binary


def char_2_num(letter: str) -> int:
    return ord(letter) - ord('a')


def num_2_char(number: int) -> str:
    return chr(ord('a') + number)


def mod(a, b):
    return a % b


def left_circ_shift(binary: str, shift: int) -> str:
    shift = shift % len(binary)
    return binary[shift:] + binary[0: shift]

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


''' ########################## FOR TESTING SOLO ###############################


# We can create an expansion box that will expand 32 Bits --> 48 Bits
expansion_p_box = PBox.des_single_round_expansion()
permutation = expansion_p_box.permutate(int_to_bin(1234, block_size=32))
print('Permutation:', permutation)
print('Output Length:', len(permutation))

# We can create a straight P-Box
straight_p_box = PBox.from_list([4, 1, 3, 2])
p = straight_p_box.permutate('help')
print(p)

# we can also create compression P-Boxes
compression_box = PBox.from_list([3, 3, 2, 1])
p = compression_box.permutate('love')
print(p)
'''


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

s_box = SBox(block_size=2, table={
    (0, 0): 5,
    (0, 1): 6,
    (1, 0): 8,
    (1, 1): 7
}, func=lambda x: (x[0], x[1]))


################################## FOR TESTING SOLO

#print(s_box('00'))
#print(s_box('01'))
#print(s_box('10'))
#print(s_box('11'))

#s_box2 = SBox.des_s_box1()
#binary = '000100'
#print(s_box2(binary))

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


################# FOR TESTING SOLO ####################

##### mixer = Mixer.des_mixer(key=3)
###### number = 1001
######## binary = int_to_bin(number, block_size=64)
####### print('Plaintext:', binary)


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

class Swapper:
    def __init__(self, block_size=64):
        self.block_size = block_size

    def encrypt(self, binary: str) -> str:
        l, r = binary[0: self.block_size // 2], binary[self.block_size // 2:]
        return r + l

    def decrypt(self, binary: str) -> str:
        return self.encrypt(binary)


class NoneSwapper:
    def encrypt(self, binary: str) -> str:
        return binary

    def decrypt(self, binary: str) -> str:
        return binary


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
        return [int(self.encrypt(int_to_bin(ord(c), block_size=64)), base=2) for c in plaintext]

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
############## FIRST WITH NUMBERS ############
number = 1312  # DO NOT SEARCH THAT NUMBER
binary = int_to_bin(number, block_size=64)

des = DES(key=78)
ciphertext = des.encrypt(binary)
print('Plaintext:', binary)
print('Ciphertext:', ciphertext)

# Decrypting
decrypted = des.decrypt(ciphertext)
print('Decrypted:', decrypted)
print('Value:', int(decrypted, base=2))
assert number == int(decrypted, base=2) # CHECK IF DECRYPTION IS CORRECT FOR NUMBERS

############## TEXT MESSAGE EXAMPLE ############# 
message = 'We just made a wholesome DES example from scratch without any libraries!Could you imagine?'
ciphertext = des.encrypt_message(message)
print('Ciphertext:', ciphertext)

# Decryption
decrypted = des.decrypt_message(ciphertext)
print('Decrypted:', decrypted)

assert decrypted == message # CHECK IF DECRYPTION IS CORRECT 