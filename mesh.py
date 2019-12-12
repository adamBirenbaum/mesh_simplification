
from vertex import Vertex
from matrix import Matrix
from face import Face
from pair import PairKey, Pair
from triangle import Triangle
import operator


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
				vertexFaces[v1].append(f)
			except KeyError:
				vertexFaces[v1] = [f]

			try:
				vertexFaces[v2].append(f)
			except KeyError:
				vertexFaces[v2] = [f]

			try:
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
		

		
		vertexPairs = {}
		i = 0.0
		
		heap = {}
		for p in pairs:
			new_pair = pairs[p]
			heap[new_pair] = new_pair.Error()
			
			try:
				vertexPairs[new_pair.A].append(new_pair)
				vertexPairs[new_pair.B].append(new_pair)
			except KeyError:
				vertexPairs[new_pair.A] = [new_pair]
				vertexPairs[new_pair.B] = [new_pair]
	
		
		iteration = 0
		numFaces = len(self.Triangles)
		original_num_faces = float(len(self.Triangles))
		target = int(float(numFaces) *  factor)
		while numFaces > target:
			#iteration +=1
			#print('Iteration '+ str(iteration))
			pct = ((original_num_faces - target) - (numFaces - target)) / (original_num_faces - target) * 100.0
			print('% Complete: ' + str(pct)+ '%')

			p = min(heap.iteritems(), key = operator.itemgetter(1))[0]
			
			del heap[p]
			if p.Removed:
				continue

			p.Removed = True

			distinctFaces = {}
			try:
				for f in vertexFaces[p.A]:
					if not f.Removed:
						distinctFaces[f] = True
			except KeyError:
				pass
			try:

				for f in vertexFaces[p.B]:
					if not f.Removed:
						distinctFaces[f] = True
			except KeyError:
					pass
			


			distinctPairs = {}
			try:
				for q in vertexPairs[p.A]:
					if not q.Removed:
						distinctPairs[q] = True
			except KeyError:
				pass
			try:
				for q in vertexPairs[p.B]:
					if not q.Removed:
						distinctPairs[q] = True
			except KeyError:
				pass
			v = Vertex(p.Vector(), p.Quadric())


			newFaces = []
			valid = True
			for f in distinctFaces:
				v1,v2,v3 = f.V1, f.V2, f.V3
				

				if v1 == p.A or v1 == p.B:
					v1 = v
				
				if v2 == p.A or v2 == p.B:
					v2 = v
				
				if v3 == p.A or v3 == p.B:
					v3 = v
				
				face = Face(v1, v2, v3)
				if face.Degenerate():
					continue
				
				if face.Normal().Dot(f.Normal()) < 1e-3:
					
					valid = False
					break
				
			
				newFaces.append(face)

			
			
			if not valid:
				continue

			try:

				del vertexFaces[p.A]
			except KeyError:
				pass

			try:
				del vertexFaces[p.B]
			except KeyError:
				pass			


			for f in distinctFaces:
				f.Removed = True
				numFaces -= 1

			for f in newFaces:
				numFaces +=1
				try:
					vertexFaces[f.V1].append(f)
					vertexFaces[f.V2].append(f)
					vertexFaces[f.V3].append(f)
				except KeyError:
					vertexFaces[f.V1] = [f]
					vertexFaces[f.V2] = [f]
					vertexFaces[f.V3] = [f]

			try:
				del vertexPairs[p.A]
			except KeyError:
				pass

			try:
				del vertexPairs[p.B]
			except KeyError:
				pass


			seen = {}

			for q in distinctPairs:
				q.Removed = True
				try:
					del heap[q]
				except KeyError:
					pass

				a,b = q.A, q.B

				if a == p.A or a == p.B:
					a = v

				if b == p.A or b == p.B:
					b = v

				if b == v:
					a,b = b,a

				try:
					if seen[b.Vector]:
						continue
				except KeyError:
					pass

				seen[b.Vector] = True
				q = Pair(a,b)
				heap[q]=q.Error()

				try:
					vertexPairs[a].append(q)
					vertexPairs[b].append(q)
				except KeyError:
					vertexPairs[a] = [q]
					vertexPairs[b] = [q]

		distinctFaces = {}
		for faces in vertexFaces.values():
			for f in faces:
				if not f.Removed:
					distinctFaces[f] = True
		
		triangles = [Triangle(f.V1.Vector, f.V2.Vector, f.V3.Vector) for f in distinctFaces if not f.Removed]

		return triangles

