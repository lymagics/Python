"""RSA public-key cryptosystem
   key: 1,024 bit(number of bits in the modulus)
   pair of primes of roughly 512 bits
"""
import random 


#Encode to num function
def encode_to_num(text):
	num_message = []
	for symbol in text:
		num_message.append(ord(symbol))
	return num_message


#Encode to symbol function
def encode_to_symbol(num_text):
	text_message = ''
	for num in num_text:
		text_message += chr(num)
	return text_message


#Miller-rabin prime test
def miller_rabin(n, k):

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


#Generate odd number for prime generator
def generate_odd(n_bits):
	num = random.randint(2**(n_bits-1),2**n_bits-1)
	if num % 2 == 0:
		num += 1
	return num


#Prime number generator function
def generate_prime(n_bits):
	while True:
		num = generate_odd(n_bits)
		if miller_rabin(num,40):
			return num


#Fast exponentiation function
def mod_power(number,degree,mod):
	res = 1
	while degree > 0:
		if degree & 1 == 1:
			res = (res * number) % mod 
		number = (number * number) % mod 
		degree >>= 1
	return res


#Find revers element which will be our private key(based on extended euclidean algorithm)
def find_reverse(b,a):
	# a = b * q + r
	q_list = []
	q = a // b
	r = a - b * q
	q_list.append(q)
	mod = a
	while r != 0:
		a = b
		b = r 
		q = a // b 
		r = a - b * q
		q_list.append(q)

	x = [1,0]
	y = [0,1]

	for i in range(2,len(q_list)+1):
		x.append(x[i-2] - q_list[i-2]*x[i-1])
		y.append(y[i-2] - q_list[i-2]*y[i-1])

	reverse = y[len(q_list)] % mod
	
	return reverse


#Encryption function
def rsa_encrypt(num_message,open_key,mod):
	encrypted = []
	for num in num_message:
		encrypted.append(mod_power(num,open_key,mod))
	return encrypted


#Decryption function
def rsa_decrypt(encrypted,private_key,mod):
	decryted = []
	for num in encrypted:
		decryted.append(mod_power(num,private_key,mod))
	return decryted


#Main
def main():
	message = 'Hello World!'
	num_message = encode_to_num(message)
	print('Plain:',num_message)

	q = generate_prime(512)
	p = generate_prime(512)
	mod = q * p

	eiler_f = (q - 1)*(p - 1)
	e_exp = 65537
	while mod % e_exp == 0:
		e_exp = generate_prime(512)

	d_exp = find_reverse(e_exp,eiler_f)

	print('Open key:',e_exp)
	print('Private key:',d_exp)

	encrypted = rsa_encrypt(num_message,e_exp,mod)
	print('Encrypted:',encrypted)

	decryted = rsa_decrypt(encrypted,d_exp,mod)
	print('Decrypted:',decryted)
	
	pass


if __name__ == '__main__':
	main()