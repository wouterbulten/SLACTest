"""
@author Wouter Bulten
"""

class Controller(object):

	def __init__(self):
		self.iteration = 0
		self.outputEnabled = True

	def iterate(self):
		self.iteration += 1
		self.output("Iteration " + str(self.iteration))

	def setOutput(self, flag):
		self.outputEnabled = flag

	def output(self, msg):
		if(self.outputEnabled):
			print(msg)

class NetworkController(Controller):

	def __init__(self, world, nodes):

		Controller.__init__(self)

		self.world = world
		self.nodes = nodes

	def iterate(self):
		super().iterate()

		for n in self.nodes:
			x,y = n.calculateStep()
			

