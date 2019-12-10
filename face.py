
class Face():
	def __init__(self, v1, v2, v3):
		self.V1 = v1  # Class Vertex
		self.V2 = v2
		self.V3 = v3

	def Degenerate(self):
		v1 = self.V1.Vector
		v2 = self.V2.Vector
		v3 = self.V3.Vector

		return v1 == v2 or v1 == v3 or v2 == v3

	def Normal(self):
		e1 = self.V2.Sub(self.V1.Vector)
		e2 = self.V3.Sub(self.V1.Vector)

		return e1.Cross(e2).Normalize()

