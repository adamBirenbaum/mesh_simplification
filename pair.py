import math

from vector import Vector

class PairKey():
	def __init__(self, a,b):
		if b.Vector.Less(a.Vector):
			a, b = b, a

		self.A = a.Vector
		self.B = b.Vector

	def __eq__(self, other):
		return (self.A.__eq__(other.A)) and (self.B.__eq__(other.B))

	def __hash__(self):
		return hash((self.A, self.B))


class Pair():
	def __init__(self, a, b):
		if b.Vector.Less(a.Vector):
			a, b = b, a

		self.A = a
		self.B = b
		self.Index = -1
		self.Removed = False
		self.CachedError =  -1

	def __eq__(self, other):
		return (self.A.__eq__(other.A)) and (self.B.__eq__(other.B))

	def __hash__(self):
		return hash((self.A, self.B))

	def get_boundary_normal(self,face):
		if self.is_boundary:
			v1 = self.A.vector
		v2 = self.B.vector
		if v1.less(v2):
			v1,v2 = v2,v1

		n = face.normal().cross(v1.subtract(v2)).normalize()


	def boundary_quadric(self,face):
		v1 = self.A.vector
		v2 = self.B.vector
		if v1.less(v2):
			v1,v2 = v2,v1
		
		n = face.normal().cross(v1.subtract(v2)).normalize()
		x,y,z = v1.x, v1.y, v1.z
		a,b,c = n.x, n.y, n.z
		d = -a*x - b*y - c*z
		
		penalty = 10000

		return Matrix(a*a, a*b, a*c,a*d, a*b, b*b, b*c, b*d, a*c, b*c, c*c, C*d, a*d, b*d, c*d, d*d).multiply_scalary(penalty)

	def Quadric(self):
		return self.A.Quadric.Add(self.B.Quadric) # Matrix

	def Vector(self):
		q = self.Quadric()

		if abs(q.der_quadric_matrix().Determinant()) > .001:
			v = q.QuadricVector()
			if (not math.isnan(v.X)) and (not math.isnan(v.Y)) and (not math.isnan(v.Z)):
				return v

		# otherwise look for best vector along edge
		n = 10

		a = self.A.Vector
		b = self.B.Vector
		d = b.Sub(a)
		bestE = -1.0
		bestV = Vector(0.,0.,0.)
		for i in range(n):
			t = float(i) / n
			v = a.Add(d.MulScalar(t))
			e = q.QuadricError(v)
			if bestE < 0 or e < bestE:
				bestE = e
				bestV = v
			
		
		return bestV

	def Error(self):
		if self.CachedError < 0:
			self.CachedError = self.Quadric().QuadricError(self.Vector())

		return self.CachedError
