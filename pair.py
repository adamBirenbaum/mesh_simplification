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


	def Quadric(self):
		return self.A.Quadric.Add(self.B.Quadric) # Matrix

	def Vector(self):
		q = self.Quadric()

		if abs(q.Determinant()) > .001:
			v = q.QuadricVector()
			if (not math.isnan(v.X)) and (not math.isnan(v.Y)) and (not math.isnan(v.Z)):
				return v

		# otherwise look for best vector along edge
		n = 10

		a = self.A.Vector
		b = self.B.Vector
		d = b.Sub(a)
		bestE = -1.0
		bestV = Vector(0,0,0)
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
