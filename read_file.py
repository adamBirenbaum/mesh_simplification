import pdb
import numpy as np
import sys
#convert to format similar to work

from triangle import Triangle
from vector import Vector
from mesh import Mesh

def read_file_into_mesh(file, to_pickle = False):
	vertex_num = 0
	vertices = {}
	faces = []
	vert_key = []
	num_lines = len(open(file).readlines())
	line_num = 0.0

	print('Converting to work format...\n')
	triangles = []
	vectors = []
	for line in open(file):
		line_num += 1.0
		split_line = line.split()
	
		if split_line[0] == 'vertex':
			
		
			vectors.append(Vector(float(split_line[1]), float(split_line[2]), float(split_line[3])))


		elif split_line[0] == 'endloop':
			triangles.append(Triangle(vectors[0], vectors[1], vectors[2]))
			vectors = []

		amtDone = line_num / num_lines
		sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))




	return triangles


def make_triangles_pyqt_readable(triangles):
	vertices = [0] * len(triangles)*3
	faces = [0]*len(triangles)

	i = 0
	for t in triangles:
		vertices[i*3] = [t.V1.X, t.V1.Y, t.V1.Z]
		vertices[i*3 + 1] = [t.V2.X, t.V2.Y, t.V2.Z]
		vertices[i*3 + 2] = [t.V3.X, t.V3.Y, t.V3.Z]

		faces[i] = [i*3, i*3 + 1, i*3 + 2]
		i+=1

	return vertices, faces

def pickle_out(ver, faces,iter):
	import pickle
	pickle_out1 = open('vertices_' + str(iter) + '.pickle','wb')
	pickle.dump(ver,pickle_out1)
	print('\n Wrote: ' + 'vertices_' + str(iter) + '.pickle')
	pickle_out1.close()
	pickle_out2 = open('faces_' + str(iter) + '.pickle','wb')
	pickle.dump(faces,pickle_out2)
	print('\n Wrote: ' + 'faces_' + str(iter) + '.pickle')
	pickle_out2.close()


if __name__ == '__main__':
	file = "/home/adam/3d_facets/stormtrooper/helmet-ascii.stl"
	file = "/home/adam/3d_facets/cheval.stl"

	triangles = read_file_into_mesh(file)

	iters = .51
	mesh = Mesh(triangles)
	tri = mesh.simplify(iters)
	ver, faces = make_triangles_pyqt_readable(tri)
	pickle_out(ver,faces,iters)
	pdb.set_trace()