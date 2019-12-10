
from vertex import Vertex
from matrix import Matrix
from face import Face
from pair import PairKey, Pair

import sys

import pdb

class Mesh():
	def __init__(self,triangles):
		self.Triangles = triangles

	def simplify(self, factor):

		print('\n\nCreating vector -> vertex dict...')
		vectorVertex = {}
		i = 0.0
		nn = float(len(self.Triangles))
		for t in self.Triangles:
			i+=1

			vectorVertex[t.V1] = Vertex(t.V1)
			vectorVertex[t.V2] = Vertex(t.V2)
			vectorVertex[t.V3] = Vertex(t.V3)
			
			amtDone = i /  nn
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))


		print('\n\nCalculating Quadric matrices for each vertex...')
		i = 0.0
		#accumlate quadric matrices for each vertex based on its faces
		for t in self.Triangles:
			i+=1

			q = t.Quadric()
			v1 = vectorVertex[t.V1]
			v2 = vectorVertex[t.V2]
			v3 = vectorVertex[t.V3]
			v1.Quadric = v1.Quadric.Add(q)
			v2.Quadric = v2.Quadric.Add(q)
			v3.Quadric = v3.Quadric.Add(q)

			amtDone = i /  nn
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
		

		# create faces and map vertex => faces

		vertexFaces = {}
		i = 0.0
		print('\n\nCreating Vertex -> faces dict...')
		for t in self.Triangles:
			i+=1

			v1 = vectorVertex[t.V1]
			v2 = vectorVertex[t.V2]
			v3 = vectorVertex[t.V3]
			f = Face(v1, v2, v3)
			try:
				test = len(vertexFaces[v1])
				vertexFaces[v1].append(f)
			except KeyError:
				vertexFaces[v1] = [f]

			try:
				test = len(vertexFaces[v2])
				vertexFaces[v2].append(f)
			except KeyError:
				vertexFaces[v2] = [f]

			try:
				test = len(vertexFaces[v3])
				vertexFaces[v3].append(f)
			except KeyError:
				vertexFaces[v3] = [f]



			amtDone = i /  nn
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
		

		i = 0.0
		pairs = {}
		for t in self.Triangles:
			i+=1
			v1 = vectorVertex[t.V1]
			v2 = vectorVertex[t.V2]
			v3 = vectorVertex[t.V3]
			pairs[PairKey(v1, v2)] = Pair(v1, v2)
			pairs[PairKey(v2, v3)] = Pair(v2, v3)
			pairs[PairKey(v3, v1)] = Pair(v3, v1)

			amtDone = i /  nn
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
		