#import initExample

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLMeshItem')
w.setCameraPosition(distance=700)

#g = gl.GLGridItem()
#g.scale(2,2,1)
#w.addItem(g)

import numpy as np


## Example 1:
## Array of vertex positions and array of vertex indexes defining faces
## Colors are specified per-face
import pickle
# pickle_in = open('original_vertices.pickle','rb')
# vertices = pickle.load(pickle_in, encoding = 'latin1')
# pickle_in.close()

# pickle_in = open('original_faces.pickle','rb')
# faces = pickle.load(pickle_in, encoding = 'latin1')
# pickle_in.close()

pickle_in = open('vertices_1000.pickle','rb')
vertices = pickle.load(pickle_in, encoding = 'latin1')
pickle_in.close()

pickle_in = open('faces_1000.pickle','rb')
faces = pickle.load(pickle_in, encoding = 'latin1')
pickle_in.close()

num_vertices = len(vertices)
num_faces = len(faces)

vertices2 = np.zeros((num_vertices,3))

#import pdb
#pdb.set_trace()
vertex_keys = list(vertices.keys())
for i in range(len(vertex_keys)):
    vertices2[i] = vertices[vertex_keys[i]]

faces2 = np.zeros((num_faces,3))
face_colors = np.zeros((num_faces,4))
convert_index_list = dict(zip(vertex_keys, list(range(len(vertex_keys)))))

for i in range(len(faces)):
    faces[i] = list(faces[i])
    for j in range(3):
        faces[i][j] = convert_index_list[faces[i][j]]
    faces2[i] = np.array([i for i in list(faces[i])])
    face_colors[i] = np.array([1, 1, 1, 0.2])
faces2 = faces2.astype(int)

#import pdb
#pdb.set_trace()
verts = np.array([
    [0, 0, 0],
    [2, 0, 0],
    [1, 2, 0],
    [1, 1, 1],
])
faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
])

verts = vertices2
faces = faces2
colors = np.array([
    [1, 0, 0, 0.3],
    [0, 1, 0, 0.3],
    [0, 0, 1, 0.3],
    [1, 1, 0, 0.3]
])

## Mesh item will automatically compute face normals.
m1 = gl.GLMeshItem(vertexes=verts, faces=faces,  smooth=True,  shader = 'shaded')#, color = face_colors )
#m1.translate(5, 5, 0)
#m1.setGLOptions('additive')
w.addItem(m1)


# ## Example 2:
# ## Array of vertex positions, three per face
# verts = np.empty((36, 3, 3), dtype=np.float32)
# theta = np.linspace(0, 2*np.pi, 37)[:-1]
# verts[:,0] = np.vstack([2*np.cos(theta), 2*np.sin(theta), [0]*36]).T
# verts[:,1] = np.vstack([4*np.cos(theta+0.2), 4*np.sin(theta+0.2), [-1]*36]).T
# verts[:,2] = np.vstack([4*np.cos(theta-0.2), 4*np.sin(theta-0.2), [1]*36]).T
    
# ## Colors are specified per-vertex
# colors = np.random.random(size=(verts.shape[0], 3, 4))
# m2 = gl.GLMeshItem(vertexes=verts, vertexColors=colors, smooth=False, shader='balloon', 
#                    drawEdges=True, edgeColor=(1, 1, 0, 1))
# m2.translate(-5, 5, 0)
# w.addItem(m2)



# ## Example 3:
# ## sphere

# md = gl.MeshData.sphere(rows=10, cols=20)
# #colors = np.random.random(size=(md.faceCount(), 4))
# #colors[:,3] = 0.3
# #colors[100:] = 0.0
# colors = np.ones((md.faceCount(), 4), dtype=float)
# colors[::2,0] = 0
# colors[:,1] = np.linspace(0, 1, colors.shape[0])
# md.setFaceColors(colors)
# m3 = gl.GLMeshItem(meshdata=md, smooth=False)#, shader='balloon')

# m3.translate(5, -5, 0)
# w.addItem(m3)


# # Example 4:
# # wireframe

# md = gl.MeshData.sphere(rows=4, cols=8)
# m4 = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))
# m4.translate(0,10,0)
# w.addItem(m4)

# # Example 5:
# # cylinder
# md = gl.MeshData.cylinder(rows=10, cols=20, radius=[1., 2.0], length=5.)
# md2 = gl.MeshData.cylinder(rows=10, cols=20, radius=[2., 0.5], length=10.)
# colors = np.ones((md.faceCount(), 4), dtype=float)
# colors[::2,0] = 0
# colors[:,1] = np.linspace(0, 1, colors.shape[0])
# md.setFaceColors(colors)
# m5 = gl.GLMeshItem(meshdata=md, smooth=True, drawEdges=True, edgeColor=(1,0,0,1), shader='balloon')
# colors = np.ones((md.faceCount(), 4), dtype=float)
# colors[::2,0] = 0
# colors[:,1] = np.linspace(0, 1, colors.shape[0])
# md2.setFaceColors(colors)
# m6 = gl.GLMeshItem(meshdata=md2, smooth=True, drawEdges=False, shader='balloon')
# m6.translate(0,0,7.5)

# m6.rotate(0., 0, 1, 1)
# #m5.translate(-3,3,0)
# w.addItem(m5)
# w.addItem(m6)



    


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()