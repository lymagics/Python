"""RC4 stream cipher
   key: 40 – 2,048 bit
"""

#Encode symbol to num
def encode_to_num(text:str):
    num_arr = []
    for letter in text:
        num_arr.append(ord(letter))
    return num_arr


#Encode num to symbol
def encode_to_symbol(num_arr:int):
    text = ''
    for num in num_arr:
        text += chr(num)
    return text


#Initialization of sbox
def sbox_initialize(key:int):
    S = []
    for i in range(256):
        S.append(i)

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%len(key)])%256
        S[i],S[j] = S[j],S[i]
    
    return S


#Pseudo-random word generation
def pseudo_random_generation(key:int,msg_len:int):
    S = sbox_initialize(key)
    K = []

    i = 0
    j = 0
    while len(K) < msg_len:
        i = (i+1) % 256
        j = (j+S[i]) % 256
        S[i],S[j] = S[j],S[i]
        t = (S[i] + S[j]) % 256
        K.append(S[t])
    
    return K


#RC4 encryption
def rc4_encrypt(key:int,msg:int):
    encrypted = []
    for i in range(0,len(msg)):
        encrypted.append(msg[i]^key[i])
    
    return encrypted


#RC4 decrypt
def rc4_decrypt(key:int,encrypted_msg:int):
    decrypted = []
    for i in range(0,len(encrypted_msg)):
        decrypted.append(encrypted_msg[i]^key[i])
    
    return decrypted


#Main
def main():
    msg = 'Hello World!'
    print('Input message:',msg)
    num_msg = encode_to_num(msg)
    seed = 'key_rc4'

    pseudo_random_key = pseudo_random_generation(encode_to_num(seed),len(num_msg))
    encrypted = rc4_encrypt(pseudo_random_key,num_msg)
    print('Encrypted:',encode_to_symbol(encrypted))

    decrypted = rc4_decrypt(pseudo_random_key,encrypted)
    print('Decrypted:',encode_to_symbol(decrypted))
    pass


if __name__ == '__main__':
    main()