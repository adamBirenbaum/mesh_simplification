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


if __name__ == '__main__':
	file = "/home/adam/3d_facets/stormtrooper/helmet-ascii.stl"
	triangles = read_file_into_mesh(file)

	mesh = Mesh(triangles)
	mesh.simplify(.5)
	pdb.set_trace()