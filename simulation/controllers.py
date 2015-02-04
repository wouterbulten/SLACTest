"""
@author Wouter Bulten
"""

class Controller(object):

	def __init__(self):
		self.iteration = 0

class NetworkController(Controller):

	def __init__(self, world, nodes):

		Controller.__init__(self)

		self.world = world
		self.nodes = nodes

	def iterate(self):
