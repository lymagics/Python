"""MD4(Message Digest 4) hash function
   output: 128 bit
"""

MASK_32 = 0x100000000
BLOCK_SIZE = 64


def F(X, Y, Z):
	return (X & Y) | ((~X) & Z)


def G(X, Y, Z):
	return (X & Y) | (X & Z) | (Y & Z)


def H(X, Y, Z):
	return (X ^ Y ^ Z)


def lshift(word32b: int, shift: int) -> int:
	return (word32b << shift) | (word32b >> (32 - shift))


def round1(A:int, B:int, C:int, D:int, k:int, s:int) -> int:
	return lshift((A + F(B, C, D) + k) % MASK_32, s)


def round2(A:int, B:int, C:int, D:int, k:int, s:int) -> int:
	return lshift((A + G(B, C, D) + k + 0x5A827999) % MASK_32, s)


def round3(A:int, B:int, C:int, D:int, k:int, s:int) -> int:
	return lshift((A + H(B, C, D) + k + 0x6ED9EBA1) % MASK_32, s)


def to_num(text: str) -> list[int]:
	return list(map(ord, text))


def append_pading_bits(num_message: list[int]) -> list[int]:
	num_message.append(0x80)
	while((len(num_message)*8) % 512 != 448):
		num_message.append(0)
	return num_message


def append_length(num_message: list[int], initial_len: int) -> list[int]:
	return num_message+list((initial_len*8).to_bytes(8, 'little'))


def make_32block(num_message: list[int]) -> list[int]:
	block32b = []
	for i in range(0, len(num_message), 4):
		block32b.append((num_message[i]) | (num_message[i+1] << 8) | (num_message[i+2] << 16) | (num_message[i+3] << 24))
	return block32b
	

def process_block(num_message: list[int]) -> None:
	N = len(num_message)
	A = 0x67452301
	B = 0xefcdab89
	C = 0x98badcfe
	D = 0x10325476
	for i in range(N // BLOCK_SIZE):
		X = make_32block(num_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE])
		AA = A
		BB = B
		CC = C
		DD = D

		#Round 1
		A = round1(A, B, C, D, X[0], 3) 
		D = round1(D, A, B, C, X[1], 7)
		C = round1(C, D, A, B, X[2], 11)
		B = round1(B, C, D, A, X[3], 19)

		A = round1(A, B, C, D, X[4], 3)
		D = round1(D, A, B, C, X[5], 7)
		C = round1(C, D, A, B, X[6], 11)
		B = round1(B, C, D, A, X[7], 19)

		A = round1(A, B, C, D, X[8], 3)
		D = round1(D, A, B, C, X[9], 7)
		C = round1(C, D, A, B, X[10], 11)
		B = round1(B, C, D, A, X[11], 19)

		A = round1(A, B, C, D, X[12], 3)
		D = round1(D, A, B, C, X[13], 7)
		C = round1(C, D, A, B, X[14], 11)
		B = round1(B, C, D, A, X[15], 19)
	
		#Round 2
		A = round2(A, B, C, D, X[0], 3)
		D = round2(D, A, B, C, X[4], 5)
		C = round2(C, D, A, B, X[8], 9)
		B = round2(B, C, D, A, X[12], 13)

		A = round2(A, B, C, D, X[1], 3)
		D = round2(D, A, B, C, X[5], 5)
		C = round2(C, D, A, B, X[9], 9)
		B = round2(B, C, D, A, X[13], 13)

		A = round2(A, B, C, D, X[2], 3)
		D = round2(D, A, B, C, X[6], 5)
		C = round2(C, D, A, B, X[10], 9)
		B = round2(B, C, D, A, X[14], 13)

		A = round2(A, B, C, D, X[3], 3)
		D = round2(D, A, B, C, X[7], 5)
		C = round2(C, D, A, B, X[11], 9)
		B = round2(B, C, D, A, X[15], 13)
	
		#Round 3
		A = round3(A, B, C, D, X[0], 3)
		D = round3(D, A, B, C, X[8], 9)
		C = round3(C, D, A, B, X[4], 11)
		B = round3(B, C, D, A, X[12], 15)

		A = round3(A, B, C, D, X[2], 3)
		D = round3(D, A, B, C, X[10], 9)
		C = round3(C, D, A, B, X[6], 11)
		B = round3(B, C, D, A, X[14], 15)

		A = round3(A, B, C, D, X[1], 3)
		D = round3(D, A, B, C, X[9], 9)
		C = round3(C, D, A, B, X[5], 11)
		B = round3(B, C, D, A, X[13], 15)

		A = round3(A, B, C, D, X[3], 3)
		D = round3(D, A, B, C, X[11], 9)
		C = round3(C, D, A, B, X[7], 11)
		B = round3(B, C, D, A, X[15], 15)

		A = (A + AA) % MASK_32
		B = (B + BB) % MASK_32 
		C = (C + CC) % MASK_32
		D = (D + DD) % MASK_32
		
	return [A, B, C, D]


def get_output(raw_hash: list[int]) -> str:
	hash = raw_hash[0].to_bytes(8, 'little')
	hash += raw_hash[1].to_bytes(8, 'little')
	hash += raw_hash[2].to_bytes(8, 'little')
	hash += raw_hash[3].to_bytes(8, 'little')

	res = ""
	for h in hash:
		if len(hex(h).lstrip("0x")) == 1 and hex(h).lstrip("0x") != '0':
			res += "0" + hex(h).lstrip("0x")
		else:
			res += hex(h).lstrip("0x") 
	return res


def md4(message: str) -> list[int]:
	num_message = to_num(message)
	initial_len = len(num_message)

	num_message = append_pading_bits(num_message)
	num_message = append_length(num_message, initial_len)

	hash = process_block(num_message)

	return get_output(hash)


if __name__ == '__main__':
	hash = md4('The quick brown fox jumps over the lazy dog')
	test = '1bee69a46ba811185c194762abaeae90'

	print(hash, test, sep='\t')
	print(hash == test)