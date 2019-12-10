

from matrix import Matrix
from vector import Vector

class Vertex(Vector):
	def __init__(self,v):
		self.Vector = v
		self.Quadric = Matrix(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

