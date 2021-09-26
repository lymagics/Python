sbox1 = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

sbox = [
    [15,12,	2,	10,	6,	4,	5,	0,	7,	9,	14,	13,	1,	11,	8,	3],
    [11,	6,	3,	4,	12,	15,	14,	2,	7,	13,	8,	0,	5,	10,	9,	1],
    [1,	12,	11,	0,	15,	14,	6,	5,	10,	13,	4,	8,	9,	3,	7,	2],
    [1,	5,	14,	12,	10,	7,	0,	13,	6,	2,	11,	4,	9,	3,	15,	8],
    [0,	12,	8,	9,	13,	2,	10,	11,	7,	3,	6,	5,	4,	14,	15,	1],
    [8,	0,	15,	3,	2,	5,	14,	11,	1,	10,	4,	7,	12,	9,	13,	6],
    [3,	0,	6,	15,	1,	14,	9,	2,	13,	8,	12,	4,	11,	10,	5,	7],
    [1,	10,	6,	8,	15, 11,	0,	4,	12,	3,	5,	9,	7,	13,	2,	14]
]

# 11111111111111111111111111111111 (32 x 1 bit)
MAX32 = 2**32-1

#Encode to num function
def encode_to_num(text:str):
    num_arr = []
    for sym in text:
        num_arr.append(ord(sym))
    return num_arr

#Encode to num russian letters function
def encode_to_num_russian(text:str):
    num_arr = []
    for sym in text:
        num_arr.append(ord(sym)-912)
    return num_arr

#Encode to symbol function
def encode_to_symbol(num_arr:int):
    text = ''
    for num in num_arr:
        text += chr(num)
    return text

#Join 8 bits array to 64 bit block
def join_8bits_to_64bits(arr_8b:int):
    block_64b = 0
    for num in arr_8b:
        block_64b <<= 8
        block_64b ^= num #|
    return block_64b

#Join two 32 bit block to one 64 bit block
def join_32bits_to_64bits(L:int,R:int):
    block_64b = (L << 32) ^ R #|
    return block_64b

#Join 8 bits array to 256 bit block
def join_8bits_to_256bits(arr_8b:int):
    block_256b = 0
    for num in arr_8b:
        block_256b <<= 8
        block_256b ^= num #|
    return block_256b

#Join 4 bits array to 32 bit block
def join_4bits_to_32bits(arr_4b:int):
    block_32b = 0
    for num in arr_4b:
        block_32b <<= 4
        block_32b ^= num #|
    return block_32b

#Split 64 bit block to 8 bits array
def split_64bits_to_8bits(block_64b:int):
    arr_8b = []
    for shift in range(56,-1,-8):
        temp = block_64b >> shift
        temp &= 255
        arr_8b.append(temp)
    return arr_8b

#Split 256 bits block to 32 bits array
def split_256_bits_to_32bits(block_256b:int):
    arr_32b = []
    for shift in range(224,-1,-32):
        temp = block_256b >> shift
        temp &= MAX32
        arr_32b.append(temp)
    return arr_32b

#Split 64 bits block on two 32 bits block
def split_64bits_to_32bits(block_64b:int):
    R = block_64b & MAX32
    L = block_64b >> 32
    return L,R

#Split 32 bits to 4 bits array
def split_32bits_to_4bits(block_32b:int):
    arr_4b = []
    for i in range(28,-1,-4):
        temp = block_32b >> i
        temp &= 15
        arr_4b.append(temp)
    return arr_4b


#Adds missing characters to massage to make it multiple of eight
def convert_to_8(num_msg:int):
    msg_len = len(num_msg)
    missing = 0
    while (msg_len % 8 == 0) == False:
        msg_len += 1
        missing += 1
    for i in range(missing):
        num_msg.append(0)
    return num_msg,missing

#Join input message to 64 bits blocks
def join_input_message_to_64bits(msg_arr:int):
    message_64b = []
    for i in range(0,len(msg_arr),8):
        message_64b.append(join_8bits_to_64bits(msg_arr[i:i+8]))
    return message_64b

#Sblock permutation
def s_permutation(arr_4b:int):
    new_arr_4b = []
    for i in range(0,8):
        new_arr_4b.append(sbox[i][arr_4b[i]]&15)
    return new_arr_4b

#Final permutation
def permutation(block_32b:int):
    arr_4b = split_32bits_to_4bits(block_32b)
    new_arr_4b = s_permutation(arr_4b)
    new_block_32b = join_4bits_to_32bits(new_arr_4b)
    return new_block_32b

#lshift block
def lshift(block:int,shift:int):
    return ((block << shift) ^ (block >> 32-shift))&MAX32 #|

def _f(part:int,key:int):
    part = part^key #temp = part^key
    part = permutation(part)
    part = lshift(part,11)
    return part

def round_feistel_encrypt(L:int,R:int,key:int):
    return R,L^_f(R,key) 

def round_feistel_decrypt(L:int,R:int,key:int):
    return R ^ _f(L,key),L

def gost_encrypt(block:int,keys:int):
    L,R = split_64bits_to_32bits(block)
    for i in range(24):
        L,R = round_feistel_encrypt(L,R,keys[i%8])
    for i in range(8):
        L,R = round_feistel_encrypt(L,R,keys[7-i])
    return join_32bits_to_64bits(L,R)

def gost_decrypt(block:int,key:int):
    L,R = split_64bits_to_32bits(block)
    for i in range(8):
        L,R = round_feistel_decrypt(L,R,key[i])
    for i in range(24):
        L,R = round_feistel_decrypt(L,R,key[(7-i)%8])
    return join_32bits_to_64bits(L,R)

def get_keys(key:str):
    keys = encode_to_num(key)
    return split_256_bits_to_32bits(join_8bits_to_256bits(keys))

def main():
    msg = 'Hello world!'
    num_msg = encode_to_num(msg)
    #num_msg = encode_to_num_russian(msg)
    print('Input message:',num_msg)
    num_msg,missing =convert_to_8(num_msg)
    num_msg = join_input_message_to_64bits(num_msg)

    key = 'this_is_a_key_for_gost_28_147_89'
    keys = get_keys(key)

    encrypted = []
    for block in num_msg:
        encrypted.append(gost_encrypt(block,keys))
    
    encrypted_8b = []
    for block in encrypted:
        encrypted_8b.append(split_64bits_to_8bits(block))

    result = []
    for block in encrypted_8b:
        for el in block:
            result.append(el)
       
    print('Encrypted message:',result)

    decrypted = []
    for block in encrypted:
        decrypted.append(gost_decrypt(block,keys))
    
    decrypted_8b = []
    for block in decrypted:
        decrypted_8b.append(split_64bits_to_8bits(block))

    result = []
    for block in decrypted_8b:
        for el in block:
            result.append(el)
    print('Decrypted message:',result)
    

main()