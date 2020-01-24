
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

		
			v1 = vectorVertex[t.V1]
			v2 = vectorVertex[t.V2]
			v3 = vectorVertex[t.V3]
			q1 = t.Quadric(t.V1)
			q2 = t.Quadric(t.V2)
			q3 = t.Quadric(t.V3)

			v1.Quadric = v1.Quadric.Add(q1)
			v2.Quadric = v2.Quadric.Add(q2)
			v3.Quadric = v3.Quadric.Add(q3)

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
		print('\n\nCreating pairs...')
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
		

		pairSharedFaces = {}
		i = 0.0
		n2 = len(pairs.values())
		print('\n\nFinding boundary faces...')
		for p in pairs.values():
			i+=1
			pairSharedFaces[p] = list(set(vertexFaces[p.A]).intersection(set(vertexFaces[p.B])))

			amtDone = i /  n2
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))

		n_one = 0
		n_two = 0
		n2 = len(pairSharedFaces.values())
		i = 0.0
		print('\n\nAdding penalty to boundary pairs...')
		for p,f in zip(pairSharedFaces.keys(), pairSharedFaces.values()):
			i+=1
			if len(f) == 1:
				boundary_q = p.boundary_quadric(f[0])
				p.A.Q = p.A.Q.add(boundar_Q)
				p.B.Q = p.B.Q.add(boundary_qq)
				n_one+=1
			else:
				n_two +=1
			amtDone = i /  n2
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))		

		
		vertexPairs = {}
		i = 0.0
		n = len(pairs)
		heap = {}
		print('\n\nAdding pairs to heap...')
		for p in pairs:
			i+=1
			new_pair = pairs[p]
			heap[new_pair] = new_pair.Error()
			
			try:
				vertexPairs[new_pair.A].append(new_pair)
			except KeyError:
				vertexPairs[new_pair.A] = [new_pair]

			try:
				vertexPairs[new_pair.B].append(new_pair)
			except KeyError:
				vertexPairs[new_pair.B] = [new_pair]
			amtDone = i /  n
			sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))	

		iteration = 0
		numFaces = len(self.Triangles)
		original_num_faces = float(len(self.Triangles))
		target = int(float(numFaces) *  factor)
		while numFaces > target:
			iteration +=1
			print('\nIteration '+ str(iteration))
			pct = ((original_num_faces - target) - (numFaces - target)) / (original_num_faces - target) * 100.0
			print('% Complete: ' + str(pct)+ '%')

			try:
				p = min(heap.iteritems(), key = operator.itemgetter(1))[0]
			except ValueError:
				break

			
			del heap[p]
			if p.Removed:
				continue

			p.Removed = True

			distinctFaces = set()
			for f in vertexFaces[p.A]:
				if not f.Removed:
					distinctFaces.add(f)

			for f in vertexFaces[p.B]:
				if not f.Removed:
					distinctFaces.add(f)



			distinctPairs = set()
			for q in vertexPairs[p.A]:
				if not q.Removed:
					distinctPairs.add(q)

			distinctPairs = set()
			for q in vertexPairs[p.B]:
				if not q.Removed:
					distinctPairs.add(q)



			v = Vertex(p.Vector(), p.Quadric())


			newFaces = []
			new_face_verts = set()
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
				new_face_verts.add(face.V1)
				new_face_verts.add(face.V2)
				new_face_verts.add(face.V3)

			
			
			if not valid:
				continue

			del vertexFaces[p.A]

			del vertexFaces[p.B]
		


			for f in distinctFaces:
				f.Removed = True
				numFaces -= 1

			for f in newFaces:
		
				numFaces +=1
				try:
					vertexFaces[f.V1].append(f)
				except KeyError:
					vertexFaces[f.V1] = [f]
				
				try:
					vertexFaces[f.V2].append(f)
				except KeyError:
					vertexFaces[f.V2] = [f]


				try:
					vertexFaces[f.V3].append(f)
				except KeyError:
					vertexFaces[f.V3] = [f]


			del vertexPairs[p.A]


			del vertexPairs[p.B]


			seen = set()

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


				if b.Vector in seen:
						continue
				if a not in new_face_verts or b not in new_face_verts:
					continue

				if a == b:
					continue

				seen.add(b.Vector)
				q = Pair(a,b)
				heap[q]=q.Error()

				try:
					vertexPairs[a].append(q)
				except KeyError:
					vertexPairs[a] = [q]
				try:
					vertexPairs[b].append(q)
				except KeyError:
					vertexPairs[b] = [q]

		distinctFaces = {}
		for faces in vertexFaces.values():
			for f in faces:
				if not f.Removed:
					distinctFaces[f] = True
		
		triangles = [Triangle(f.V1.Vector, f.V2.Vector, f.V3.Vector) for f in distinctFaces if not f.Removed]

		return triangles

