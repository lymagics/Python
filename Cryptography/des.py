"""DES block cipher
   key: 56 bit
   block: 64 bit
"""


MAX32 = 2**32-1
MAX28 = 2**28-1


E = [
    32,	1,	2,	3,	4,	5,
    4,	5,	6,	7,	8,	9,
    8,	9,	10,	11,	12,	13,
    12,	13,	14,	15,	16,	17,
    16,	17,	18,	19,	20,	21,
    20,	21,	22,	23,	24,	25,
    24,	25,	26,	27,	28,	29,
    28,	29,	30,	31,	32,	1
]


sbox = [
    [#Sbox 1
    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,	6,	12,	11,	9,	5,	3,	8],
    [4,	1,	14,	8,	13,	6,	2,	11,	15,	12,	9,	7,	3,	10,	5,	0],
    [15,	12,	8,	2,	4,	9,	1,	7,	5,	11,	3,	14,	10,	0,	6,	13]
    ],
    [#Sbox 2
    [15,	1,	8,	14,	6,	11,	3,	4,	9,	7,	2,	13,	12,	0,	5,	10],
    [3,	13,	4,	7,	15,	2,	8,	14,	12,	0,	1,	10,	6,	9,	11,	5],
    [0,	14,	7,	11,	10,	4,	13,	1,	5,	8,	12,	6,	9,	3,	2,	15],
    [13,	8,	10,	1,	3,	15,	4,	2,	11,	6,	7,	12,	0,	5,	14,	9]
    ],
    [#Sbox 3
    [10,	0,	9,	14,	6,	3,	15,	5,	1,	13,	12,	7,	11,	4,	2,	8],
    [13,	7,	0,	9,	3,	4,	6,	10,	2,	8,	5,	14,	12,	11,	15,	1],
    [13,	6,	4,	9,	8,	15,	3,	0,	11,	1,	2,	12,	5,	10,	14,	7],
    [1,	10,	13,	0,	6,	9,	8,	7,	4,	15,	14,	3,	11,	5,	2,	12]
    ],
    [#Sbox 4
    [7,	13,	14,	3,	0,	6,	9,	10,	1,	2,	8,	5,	11,	12,	4,	15],
    [13,	8,	11,	5,	6,	15,	0,	3,	4,	7,	2,	12,	1,	10,	14,	9],
    [10,	6,	9,	0,	12,	11,	7,	13,	15,	1,	3,	14,	5,	2,	8,	4],
    [3,	15,	0,	6,	10,	1,	13,	8,	9,	4,	5,	11,	12,	7,	2,	14]
    ],
    [#Sbox 5
    [2,	12,	4,	1,	7,	10,	11,	6,	8,	5,	3,	15,	13,	0,	14,	9],
    [14,	11,	2,	12,	4,	7,	13,	1,	5,	0,	15,	10,	3,	9,	8,	6],
    [4,	2,	1,	11,	10,	13,	7,	8,	15,	9,	12,	5,	6,	3,	0,	14],
    [11,	8,	12,	7,	1,	14,	2,	13,	6,	15,	0,	9,	10,	4,	5,	3]
    ],
    [#Sbox 6
    [12,	1,	10,	15,	9,	2,	6,	8,	0,	13,	3,	4,	14,	7,	5,	11],
    [10,	15,	4,	2,	7,	12,	9,	5,	6,	1,	13,	14,	0,	11,	3,	8],
    [9,	14,	15,	5,	2,	8,	12,	3,	7,	0,	4,	10,	1,	13,	11,	6],
    [4,	3,	2,	12,	9,	5,	15,	10,	11,	14,	1,	7,	6,	0,	8,	13	]
    ],
    [#Sbox 7
    [4,	11,	2,	14,	15,	0,	8,	13,	3,	12,	9,	7,	5,	10,	6,	1],
    [13,	0,	11,	7,	4,	9,	1,	10,	14,	3,	5,	12,	2,	15,	8,	6],
    [1,	4,	11,	13,	12,	3,	7,	14,	10,	15,	6,	8,	0,	5,	9,	2],
    [6,	11,	13,	8,	1,	4,	10,	7,	9,	5,	0,	15,	14,	2,	3,	12]
    ],
    [#Sbox 8
    [13,	2,	8,	4,	6,	15,	11,	1,	10,	9,	3,	14,	5,	0,	12,	7],
    [1,	15,	13,	8,	10,	3,	7,	4,	12,	5,	6,	11,	0,	14,	9,	2],
    [7,	11,	4,	1,	9,	12,	14,	2,	0,	6,	10,	13,	15,	3,	5,	8],
    [2,	1,	14,	7,	4,	10,	8,	13,	15,	12,	9,	0,	3,	5,	6,	11]
    ]
]


P = [16,	7,	20,	21,	29,	12,	28,	17,
    1,	15,	23,	26,	5,	18,	31,	10,
    2,	8,	24,	14,	32,	27,	3,	9,
    19,	13,	30,	6,	22,	11,	4,	25
]


KP1 = [
    57,	49,	41,	33,	25,	17,	9,	1,	58,	50,	42,	34,	26,	18,
    10,	2,	59,	51,	43,	35,	27,	19,	11,	3,	60,	52,	44,	36
]


KP2 = [
    63,	55,	47,	39,	31,	23,	15,	7,	62,	54,	46,	38,	30,	22,
    14,	6,	61,	53,	45,	37,	29,	21,	13,	5,	28,	20,	12,	4
]


KCP = [
    14,	17,	11,	24,	1,	5,	3,	28,	15,	6,	21,	10,	23,	19,	12,	4,
    26,	8,	16,	7,	27,	20,	13,	2,	41,	52,	31,	37,	47,	55,	30,	40,
    51,	45,	33,	48,	44,	49,	39,	56,	34,	53,	46,	42,	50,	36,	29,	32
]


IP = [
    58,	50,	42,	34,	26,	18,	10,	2,	60,	52,	44,	36,	28,	20,	12,	4,
    62,	54,	46,	38,	30,	22,	14,	6,	64,	56,	48,	40,	32,	24,	16,	8,
    57,	49,	41,	33,	25,	17,	9,	1,	59,	51,	43,	35,	27,	19,	11,	3,
    61,	53,	45,	37,	29,	21,	13,	5,	63,	55,	47,	39,	31,	23,	15,	7
]


FP = [
    40,	8,	48,	16,	56,	24,	64,	32,	39,	7,	47,	15,	55,	23,	63,	31,
    38,	6,	46,	14,	54,	22,	62,	30,	37,	5,	45,	13,	53,	21,	61,	29,
    36,	4,	44,	12,	52,	20,	60,	28,	35,	3,	43,	11,	51,	19,	59,	27,
    34,	2,	42,	10,	50,	18,	58,	26,	33,	1,	41,	9,	49,	17,	57,	25
]


#Encode to num function
def encode_to_num(text:str):
    num_arr = []
    for letter in text:
        num_arr.append(ord(letter))
    return num_arr


#Encode to symbol function
def encode_to_symbol(num_arr:int):
    text = ''
    for num in num_arr:
        text+=chr(num)
    return text


#Complite block less than 64 bit with adding zeros to the end
def complite_block(num_arr:int):
    missing = 0
    length = len(num_arr)
    while length%8 != 0:
        length += 1
        missing += 1
    for i in range(missing):
        num_arr.append(0)
    return num_arr


#Join 8 bits array to 64 bit block
def join_8bits_to_64bits(arr8b:int):
    block_64b = 0
    for num in arr8b:
        block_64b <<= 8
        block_64b |= num
    return block_64b


#Join two 32 bit block to one 64 bit block
def join_32bits_to_64bits(L:int,R:int):
    return (L << 32) ^ R


#Join input text to 64 bit blocks
def join_input_to_64bits(num_arr:int):
    block_64b = []
    for i in range(0,len(num_arr),8):
        block_64b.append(join_8bits_to_64bits(num_arr[i:i+8]))
    return block_64b


#Split 64 bits block on two 32 bits block
def split_64bits_to_32bits(block64b:int):
    L = (block64b >> 32)
    R = block64b & MAX32
    return L,R


#Split 64 bit block to 8 bits array
def split_64bits_to_8bits(block64:int):
    arr_8 = []
    for i in range(56,-1,-8):
        arr_8.append((block64 >> i)&0b11111111)
    return arr_8


#Split 32 bit block to 4 bits array
def split_32bits_to_4bits(block32b:int):
    arr_4b = []
    for shift in range(28,-1,-4):
        temp = (block32b >> shift) & 0b1111
        arr_4b.append(temp)
    return arr_4b


#Split 48 bit block to 6 bits array
def split_48bits_to_6bits(block_48:int):
    arr_6bits = []
    for shift in range(42,-1,-6):
        temp = (block_48 >> shift) & 0b111111
        arr_6bits.append(temp)
    return arr_6bits


#Join 4 bits array to 32 bit block
def join_4bits_to_32bits(arr_4b:int):
    block_32b = 0
    for num in arr_4b:
        block_32b <<= 4
        block_32b |= num
    return block_32b


#Join two 28 bit blocks to one 56 bit
def join_28bits_to_56bits(C:int,D:int):
    return ((C << 28) | D)


#Expand 4 bit block to 6 bit block
def expand_4bits_to_6bits(arr_4b):
    arr_6b = []
    for i in range(8):
        pred = i - 1
        next = i + 1
        if i == 0:
            pred = 7
        if i == 7:
            next = 0
        temp = ((arr_4b[pred] << 5)|(arr_4b[i] << 1)|(arr_4b[next] >> 3))&0b111111
        arr_6b.append(temp)
    return arr_6b


#Get extra and middle bits 011110 -> extra 00 middle 1111
def get_extra_and_middle_bits(_6b):
    extra = (_6b&0b000001) | ((_6b&0b100000) >> 4)
    middle = (_6b&0b011110) >> 1
    return extra,middle


#Subtitution function
def subtitution(block_6b:int):
    arr_4b = []
    for i in range(8):
        extra,middle = get_extra_and_middle_bits(block_6b[i])
        arr_4b.append(sbox[i][extra][middle])
    return arr_4b


#Permutation function
def permutation(b_32:int):
    new_b32 = 0
    for i in range(32):
        new_b32 <<= 1
        new_b32 = new_b32 | ((b_32 >> (P[i]-1))&0b01)
    return new_b32


#Pertumes key 56 bit to 28 bit
def key_permutation_56bits_to_28bits(key_64b:int):
    C,D = 0,0
    for i in range(28):
        C <<= 1
        D <<= 1
        C |= ((key_64b >> (64 - KP1[i]))&0b01) 
        D |= ((key_64b >> (64 - KP2[i]))&0b01) 
    return C,D


#Constructs key from 56 bit to 48 bit
def key_construction_permutation(block_56b:int):
    key_48b = 0
    for i in range(48):
        key_48b <<= 1
        key_48b |= (block_56b >> (KCP[i]-1))&0b01
    return key_48b


#Expand 32 bit block to 48 bit
def expansion(block_32b:int):
    block_48b = 0
    for i in range(48):
        block_48b <<= 1
        block_48b |= (block_32b >> (E[i]-1))&0b01
    return block_48b


#Main key generation function
def generate_key(key:int):
    key_56b = join_8bits_to_64bits(key)
    key_list = []
    C,D = key_permutation_56bits_to_28bits(key_56b)
    for i in range(16):
        n = 0
        if i in [0,1,8,15]:
            n = 1
        else:
            n = 2
        
        C = lshift(C,n)
        D = lshift(D,n)

        block_56b = join_28bits_to_56bits(C,D)
        temp_key = key_construction_permutation(block_56b)
        key_list.append(temp_key)
    return key_list


#Left bit shift
def lshift(key_28b:int,shift:int):
    return ((key_28b << shift) | (key_28b >> (28-shift)))&MAX28


#Initial permutation
def initial_permutation(block_64b:int):
    new_block64 = 0
    for i in range(64):
        new_block64 <<= 1
        new_block64 |= (block_64b >> (IP[i]-1))&0b01
    return new_block64


#Final permutation
def final_permutation(block_64b:int):
    new_block64 = 0
    for i in range(64):
        new_block64 <<= 1
        new_block64 |= (block_64b >> (FP[i]-1))&0b01
    return new_block64


#32 bit block transformation
def _f(part:int,key:int):
    part = expansion(part)
    part ^= key
    part = split_48bits_to_6bits(part)
    part = subtitution(part)
    part = join_4bits_to_32bits(part)
    return permutation(part)


#Feistel encryption round
def round_feistel_encrypt(L:int,R:int,key:int):
    return R,L^_f(R,key) 


#Feistel decryption round
def round_feistel_decrypt(L:int,R:int,key:int):
    return R ^ _f(L,key),L


#Main encryption function
def des_encrypt(block_64b:int,keys:int):
    block_64b = initial_permutation(block_64b)
    L,R = split_64bits_to_32bits(block_64b)

    for i in range(16):
        L,R = round_feistel_encrypt(L,R,keys[i])
    return final_permutation(join_32bits_to_64bits(L,R))


#Main decryption function
def des_decrypt(block_64b:int,keys:int):
    block_64b = initial_permutation(block_64b)
    L,R = split_64bits_to_32bits(block_64b)

    for i in range(15,-1,-1):
        L,R = round_feistel_decrypt(L,R,keys[i])
    return final_permutation(join_32bits_to_64bits(L,R))


#Main
def main():
    key = 'des_key_'
    num_key = encode_to_num(key)
    keys = generate_key(num_key)

    msg = 'plain text to encrypt'
    num_msg = encode_to_num(msg)
    print('Plain text:',num_msg)
    num_msg = join_input_to_64bits(complite_block(num_msg))

    encrypted = []
    for block in num_msg:
        encrypted.append(split_64bits_to_8bits(des_encrypt(block,keys)))

    encrypted_8b = []
    for block in encrypted:
        for el in block:
            encrypted_8b.append(el)

    print('Encrypted:',encrypted_8b)

    encrypted_arr = join_input_to_64bits(encrypted_8b)
    decrypted = []
    for block in encrypted_arr:
        decrypted.append(split_64bits_to_8bits(des_decrypt(block,keys)))
    
    decrypted_8b = []
    for block in decrypted:
        for el in block:
            decrypted_8b.append(el)

    print('Decrypted:',decrypted_8b)


if __name__ == '__main__':
    main()

