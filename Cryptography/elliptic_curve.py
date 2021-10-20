"""Elliptic Curve Class
   tested on P-256 elliptic curve
   https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186-draft.pdf
"""


INF_POINT = None


class EllipticCurve:
	def __init__(self,a,b,p):
		self.a = a
		self.b = b
		self.p = p


	def discriminant(self):
		return -16 * (4 * self.a ** 3 + 27 * self.b ** 2) != 0


	def mod(self,x):
		return x % self.p


	def is_point_on_curve(self,P):
		return self.mod(P[1] ** 2) == self.mod(P[0] ** 3 + self.a * P[0] + self.b)


	def reverse(self,x):
		if self.mod(x) == 0:
			return None 
		return pow(x,self.p-2,self.p)


	def is_equal(self,x,y):
		return self.mod(x - y) == 0


	def add_point(self,P1,P2):
		if P1 == INF_POINT:
			return P2
		if P2 == INF_POINT:
			return P1

		(x1,y1) = P1 
		(x2,y2) = P2 

		if self.is_equal(x1,x2) and self.is_equal(y1,-y2):
			return INF_POINT

		if self.is_equal(x1,x2) and self.is_equal(y1,y2):
			l = self.mod((3 * x1 * x1 + self.a) * self.reverse(2 * y1))
		else:
			l = self.mod((y1 - y2) * self.reverse(x1 - x2))

		v = self.mod(y1 - x1 * l)
		x3 = self.mod(l * l  - x1 - x2)
		y3 = self.mod(-l * x3 - v)
		return (x3,y3)


	def multiply(self,n,P):
		Q = INF_POINT
		while n > 0:
			if n & 1 == 1:
				Q = self.add_point(Q,P)
			P = self.add_point(P,P)
			n >>= 1
		return Q
	

def main():
	a = -3
	b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
	p = 115792089210356248762697446949407573530086143415290314195533631308867097853951 
	gx = 48439561293906451759052585252797914202762949526041747995844080717082404635286  
	gy = 36134250956749795798585127919587881956611106672985015071877198253568414405109
	n = 115792089210356248762697446949407573529996955224135760342422259061068512044369 
	G = (gx,gy)
	p256 = EllipticCurve(a,b,p)

	print(p256.is_point_on_curve(G))

	print(G == p256.multiply(1,G))

	print(INF_POINT == p256.multiply(n,G))

	#Random point on the curve
	print(p256.multiply(3,G))
	pass


if __name__ == '__main__':
	main()
