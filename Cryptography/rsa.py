def encode_to_num(text:str):
    num_arr = []
    for sym in text:
        num_arr.append(ord(sym))
    return num_arr

def encode_to_symbol(num_arr:int):
    text = ''
    for num in num_arr:
        text += chr(num)
    return text

def is_prime(num:int):
    for i in range(2,num):
        if num % i == 0:
            return False
    return True

def generate_prime():
    from random import randint
    prime = randint(2,100)
    while is_prime(prime) == False:
        prime = randint(2,100)
    return prime

def eiler_function(p:int,q:int):
    return (p - 1)*(q - 1)

def is_mutually_simple(f_num:int,s_num:int):
    if f_num > s_num:
        for i in range(2,s_num+1):
            if f_num % i == 0 and s_num % i == 0:
                return False
        return True
    if f_num < s_num:
        for i in range(2,f_num+1):
            if f_num % i == 0 and s_num % i == 0:
                return False
        return True
    if f_num == s_num:
        return False if is_prime(f_num) else True
           
def generate_e(eiler_f:int):
    e = generate_prime()
    while e < eiler_f == False and is_mutually_simple(e,eiler_f) == False:
        e = generate_prime()
    return e

def generate_d(e:int,eiler_f:int):
    from random import randint
    d = randint(2,100)
    while (d*e)%eiler_f != 1:
        d = randint(2,10000)
    return d

def encrypt(e,num_msg,mod):
    encrypted = []
    for el in num_msg:
        encrypted.append((el**e)%mod)
    return encrypted

def decrypt(d,encrypted,mod):
    decrypted = []
    for el in encrypted:
        decrypted.append((el**d)%mod)
    return decrypted

def main():
    msg = 'Hello world!'
    print('Plain text:',msg)
    num_msg = encode_to_num(msg)

    p = generate_prime()
    q = generate_prime()
    mod = p*q

    eiler_f = eiler_function(p,q)
    e = generate_e(eiler_f)
    d = generate_d(e,eiler_f)

    print('Open key:',e,mod)

    encrypted = encrypt(e,num_msg,mod)
    print('Encrypted:',encode_to_symbol(encrypted))

    decrypted = decrypt(d,encrypted,mod)
    print('Decrypted:',encode_to_symbol(decrypted))

main()