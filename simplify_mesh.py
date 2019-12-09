import pdb
import numpy as np
import sys
#convert to format similar to work
file = "/home/adam/3d_facets/stormtrooper/helmet-ascii.stl"

import pickle

# vertex_num = 0
# vertices = {}
# faces = []
# vert_key = []
# num_lines = len(open(file).readlines())
# line_num = 0.0

# print('Converting to work format...\n')
# for line in open(file):
# 	line_num += 1.0
# 	split_line = line.split()
	
# 	if split_line[0] == 'vertex':
# 		vert = tuple([float(split_line[i]) for i in range(1,4)])
# 		if vert in vertices.values():
# 			key = [key for key, value in vertices.iteritems() if value == vert][0]
# 			vert_key.append(key)
# 			# for i in range(len(vertices.values())):
# 			# 	key  = vertices.keys()[i]
# 			# 	if vertices[key] == vert:
# 			# 		vert_key.append(key)
# 			# 		break
# 		else:
# 			vertex_num+=1
# 			vertices[vertex_num] = tuple([float(split_line[i]) for i in range(1,4)])
# 			vert_key.append(vertex_num)
# 	elif split_line[0] == 'endloop':
# 		faces.append([vert_key[0],vert_key[1], vert_key[2]])
# 		vert_key =  []
# 	else:
# 		continue
# 	amtDone = line_num / num_lines
# 	sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
#
# for i in range(1,len(vertices) + 1):
# 	vertices[i] = np.array(vertices[i])
# 
# for i in range(len(faces)):
# 	faces[i] = set(faces[i])
#
# pickle_out1 = open('vertices.pickle','wb')
# pickle.dump(vertices,pickle_out1)
# pickle_out1.close()
# pickle_out2 = open('faces.pickle','wb')
# pickle.dump(faces,pickle_out2)
# pickle_out2.close()



pickle_in = open('original_vertices.pickle','rb')
vertices = pickle.load(pickle_in)
pickle_in.close()
pickle_in = open('original_faces.pickle','rb')
faces = pickle.load(pickle_in)
pickle_in.close()



num_vertices = len(vertices)
# keys = range(1, num_vertices + 1)
# vals = [[] for i in range(num_vertices)]
# edges_by_vertex = dict(zip(keys, vals))


# for i in range(1,len(vertices) + 1):
# 	for j in range(len(faces)):
# 		if i in faces[j]:
# 			edges_by_vertex[i].append([z for z in faces[j] if z != i])

# 	# if i == 10:
# 	# 	pdb.set_trace()
# 	amtDone = float(i) / float(num_vertices)
# 	sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))


# pickle_out1 = open('edges_by_vertex.pickle','wb')
# pickle.dump(edges_by_vertex,pickle_out1)
# pickle_out1.close()

pickle_in = open('edges_by_vertex.pickle','rb')
edges_by_vertex = pickle.load(pickle_in)
pickle_in.close()

#Calculate Q
# print('Calculating Q for each vertex')
# Q = {}
# for i in range(1, num_vertices + 1):
# 	v0 = vertices[i]
# 	Q_vert = np.zeros((4,4))
# 	for j in range(len(edges_by_vertex[i])):
		
# 		v1 = vertices[edges_by_vertex[i][j][0]]
# 		v2 = vertices[edges_by_vertex[i][j][1]]

# 		temp = np.cross(v1 - v0, v2 - v0)
# 		n = temp / np.linalg.norm(temp)
# 		d = -1*np.dot(n, v0)
# 		p = np.array([[n[0]],[n[1]],[n[2]],[d]])
# 		Q_vert += np.dot(p,np.transpose(p))
		
# 	Q[i] = Q_vert	
	
# 	amtDone = float(i) / float(num_vertices)
# 	sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))

# print('\nDone')

# pickle_out1 = open('Q.pickle','wb')
# pickle.dump(Q,pickle_out1)
# pickle_out1.close()


pickle_in = open('Q.pickle','rb')
Q = pickle.load(pickle_in)
pickle_in.close()


import pandas as pd

# Get valid pairs

# valid_pairs = []
# for i in range(1,num_vertices + 1):
# 	for j in range(len(edges_by_vertex[i])):
# 		new_set1 = set([i,edges_by_vertex[i][j][0]])
# 		new_set2 = set([i,edges_by_vertex[i][j][1]])

# 		if not np.any(np.array([new_set1 == z for z in  valid_pairs])):
# 			valid_pairs.append(new_set1)
# 		if not np.any(np.array([new_set2 == z for z in  valid_pairs])):
# 			valid_pairs.append(new_set2)
# 		# if new_set1 not in valid_pairs:
# 		# 	valid_pairs.append(new_set1)

# 		# if new_set2 not in valid_pairs:
# 		# 	valid_pairs.append(new_set2)
	
#  	amtDone = float(i) / float(num_vertices)
# 	sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))

# pickle_out1 = open('valid_pairs.pickle','wb')
# pickle.dump(valid_pairs, pickle_out1)
# pickle_out1.close()




pickle_in = open('valid_pairs.pickle','rb')
valid_pairs = pickle.load(pickle_in)
pickle_in.close()


ss_error_list = [0]*len(valid_pairs)
optimal_v_list = [0]*len(valid_pairs)
recalc_error = [0]*len(valid_pairs)
num_singular = 0
for i in range(len(valid_pairs)):
	edge_list = list(valid_pairs[i])
	Q_total = Q[edge_list[0]] + Q[edge_list[1]]
	Q_total[3,] = np.array([0,0,0,1])
	try:
		Q_inv = np.linalg.inv(Q_total)
		optimal_v = np.dot(Q_inv, np.array([[0],[0],[0],[1]]))
	except np.linalg.linalg.LinAlgError:
		num_singular+=1
		optimal_v = (vertices[edge_list[0]] + vertices[edge_list[1]])/2


	Q_total = Q[edge_list[0]] + Q[edge_list[1]]
	ss_error = np.dot(np.transpose(optimal_v),np.dot(Q_total, optimal_v))[0][0]
	ss_error_list[i] = ss_error

	optimal_v_list[i] = np.array([optimal_v[0][0], optimal_v[1][0], optimal_v[2][0]])
	recalc_error[i] = False
  	amtDone = float(i) / float(len(valid_pairs))
 	sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))

print('\n Done')
data = {'Valid_Pairs': valid_pairs, 'SS_Error': ss_error_list,'New_Vertex': optimal_v_list,'Recalc_Error': recalc_error}
df = pd.DataFrame(data)

iteration = 0;
stop_iteration = 5000

while True:


	if iteration == stop_iteration:
		pickle_out1 = open('vertices_5000.pickle','wb')
		pickle.dump(vertices, pickle_out1)
		pickle_out1.close()
		pickle_out1 = open('faces_5000.pickle','wb')
		pickle.dump(faces, pickle_out1)
		pickle_out1.close()
		break

	iteration +=1
	
	df = df.sort_values(by = 'SS_Error')

	min_error = df.SS_Error.values[0]
	print('Iteration: ' + str(iteration) + '  Min. Error: ' + str(min_error))
	if min_error > 100:
		pickle_out1 = open('vertices_10000.pickle','wb')
		pickle.dump(vertices, pickle_out1)
		pickle_out1.close()
		pickle_out1 = open('faces_10000.pickle','wb')
		pickle.dump(faces, pickle_out1)
		pickle_out1.close()
		break

	optimal_edge = list(df.Valid_Pairs.values[0])
	new_vertex = df.New_Vertex.values[0]
	v1 = optimal_edge[0]
	v2 = optimal_edge[1]

	vertices[v1] = new_vertex
	del vertices[v2]

	degenerate_faces = []
	for i in range(len(faces)):
		current_face = faces[i]
		if v2 in current_face:
			current_face.discard(v2)
			current_face.add(v1)

			if len(current_face) < 3:
				degenerate_faces.append(i)

	if len(degenerate_faces) > 0:
		for i in sorted(degenerate_faces, reverse = True):
			del faces[i]


	df = df.drop(df.index[0])


	valid_pairs_list = df.Valid_Pairs.values
	indexes_to_delete = []
	aa = []

	for i in range(len(df)):

		if v1 in valid_pairs_list[i]:
			df.at[df.index[i],'Recalc_Error'] = True

		if v2 in valid_pairs_list[i]:

			valid_pairs_list[i].remove(v2)
			valid_pairs_list[i].add(v1)
			if sum(np.array([valid_pairs_list[i] == z for z in  valid_pairs_list])) == 2:
				indexes_to_delete.append(i)
				aa.append(valid_pairs_list[i])
				continue

			if len(valid_pairs_list[i]) < 2:
				pdb.set_trace()
			df.at[df.index[i],'Valid_Pairs'] = valid_pairs_list[i]
			df.at[df.index[i],'Recalc_Error'] = True
	
	# if v1 == 3421:
	# 	pdb.set_trace()
	if len(indexes_to_delete) > 0:
		df = df.drop(df.index[indexes_to_delete])
	else:
		print("ASDFALSDKFSDKFJDS")
	
	# if v1 == 3421:
	# 	pdb.set_trace()
	indexes_to_recalulate = [i for i in range(len(df)) if df.Recalc_Error.values[i]]


	#Update the edges_by_vertex of v1
	edges_by_vertex[v1] = []
	for j in range(len(faces)):
		if v1 in faces[j]:
			edges_by_vertex[v1].append([z for z in faces[j] if z != v1])



	v0 = vertices[v1]
	Q_vert = np.zeros((4,4))
	for j in range(len(edges_by_vertex[v1])):
		
		vv1 = vertices[edges_by_vertex[v1][j][0]]
		vv2 = vertices[edges_by_vertex[v1][j][1]]

		temp = np.cross(vv1 - v0, vv2 - v0)
		n = temp / np.linalg.norm(temp)
		d = -1*np.dot(n, v0)
		
		p = np.array([[n[0]],[n[1]],[n[2]],[d]])
		Q_vert += np.dot(p,np.transpose(p))
			
	Q[v1] = Q_vert


	for i in indexes_to_recalulate:
		edge_list = list(valid_pairs_list[i])

		try:
			Q_total = Q[edge_list[0]] + Q[edge_list[1]]
		except IndexError:
			pdb.set_trace()
		Q_total[3,] = np.array([0,0,0,1])
		try:
			Q_inv = np.linalg.inv(Q_total)
			optimal_v = np.dot(Q_inv, np.array([[0],[0],[0],[1]]))
		except np.linalg.linalg.LinAlgError:
			num_singular+=1
			optimal_v = (vertices[edge_list[0]] + vertices[edge_list[1]])/2


		Q_total = Q[edge_list[0]] + Q[edge_list[1]]
		ss_error = np.dot(np.transpose(optimal_v),np.dot(Q_total, optimal_v))[0][0]
		df.at[df.index[i],'SS_Error'] = ss_error
		df.at[df.index[i],'New_Vertex'] = np.array([optimal_v[0][0], optimal_v[1][0], optimal_v[2][0]])
		df.at[df.index[i],'Recalc_Error'] = False






# when found denerate face indexes, loop through them backwards and delete them



