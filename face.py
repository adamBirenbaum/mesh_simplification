
class Face():
	def __init__(self, v1, v2, v3):
		
		if v1.Vector.Less(v2.Vector):
			if v2.Vector.Less(v3.Vector):
				v1,v2,v3 = v3,v2,v1
			elif v1.Vector.Less(v3.Vector):
				v1,v2,v3 = v2,v3,v2	
			else:
				v1,v2,v3 = v2,v1,v3
		elif v1.Vector.Less(v3.Vector):
			v1,v2,v3 = v3,v1,v2
		else:
			if v2.Vector.Less(v3.Vector):
				v1,v2,v3 = v1,v3,v2
			else: 
				v1,v2,v3 = v1,v2,v3




		self.V1 = v1  # Class Vertex
		self.V2 = v2
		self.V3 = v3
		self.Removed = False

	def Degenerate(self):
		v1 = self.V1.Vector
		v2 = self.V2.Vector
		v3 = self.V3.Vector

		return v1 == v2 or v1 == v3 or v2 == v3

	def Normal(self):
		e1 = self.V2.Vector.Sub(self.V1.Vector)
		e2 = self.V3.Vector.Sub(self.V1.Vector)

		return e1.Cross(e2).Normalize()




