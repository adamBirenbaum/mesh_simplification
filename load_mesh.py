from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class Plot3D()

	def __init__(self)
		app = QtGui.Qapplication.instance()
		if app is None:
			self.app = QtGui.QApplication([])
		else:
			self.app = app

		self.view = gl.GLViewWidget()
		self.view.show()
		self.view.setGeometry(300,150,1600,900)
		v = Vector(0,0,0)
		self.view.setCameraPosition(distance = 10, elevation = 30, azimuth = 45)
		self.view.opts['center'] = V

	def add_mesh(self, mesh):
		self.view.addItem(mesh)

	def start(self):
		if (sys.flags.interactive!=1 or not hasattr(QtCore, 'PYQT_VERSION'):
			self.app.instance().exec_()

if __name__ == '__main__':
	p_3d = Plot3D()
	vertices = np.loadtxt('vertices.txt')
	faces = np.loadtxt('faces.txt')

	mesh = gl.GLMeshItem(vertexes=vertices, faces=faces,  smooth=True) 
	p_3d.add_mesh(mesh)
	p_3d.start()