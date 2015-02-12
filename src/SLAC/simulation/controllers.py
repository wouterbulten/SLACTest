"""
@author Wouter Bulten
"""
import numpy as np
import math
import SLAC.network.wireless as wsn
import SLAC.environment.world as env

def generateData(xMax = 25, yMax = 25, fixedNodes = 25, noise = 2, steps = 500):
	'''
	Simulates an environment and returns Y and user
	
	:param xMax: max world size x
	:param yMax: max wolrd size y
	:param fixedNodes: amount of fixed nodes
	:param noise: noise variance
	:param steps: amount of simulation steps
	'''

	# Create a new world
	world = env.World(xMax, yMax)
	# Instantiate nodes with a random position
	nodes = [wsn.FixedAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, fixedNodes)]
	user = wsn.MovingAP(maxX = world.getMaxX(), maxY = world.getMaxY())
	nodes.append(user)
	
	# Create a network controller, containing the world and nodes
	controller = NetworkController(world, nodes, False)
	# Initialize the world, gives nodes initial speed and direction
	controller.initialize()
	
	Y = np.array([n.getSignalStrengthAtLocation(*user.getPosition(), noise=noise) for n in nodes if n != user])
	
	# Simulate movement in the network
	for i in range(0, steps):
		
		# Update the total network
		controller.iterate()
		
		# Get RSSI measurements
		rssi = [n.getSignalStrengthAtLocation(*user.getPosition(), noise=noise) for n in nodes if n != user]
		Y = np.vstack((Y, rssi))
		
	return (Y, user)

class Controller(object):

	def __init__(self, outputEnabled = True):
		self.iteration = 0
		self.outputEnabled = outputEnabled

	def iterate(self):
		self.iteration += 1
		self.output("Iteration " + str(self.iteration))

	def setOutput(self, flag):
		self.outputEnabled = flag

	def output(self, msg):
		if(self.outputEnabled):
			print(msg)

class NetworkController(Controller):

	def __init__(self, world, nodes, outputEnabled = True):

		Controller.__init__(self, outputEnabled)

		self.world = world
		self.nodes = nodes

	def initialize(self):
		
		#Initialize all nodes with random position and movement
		for n in self.nodes:
			n.initialize(*self.world.getRandomPosition())
		
	def iterate(self):
		Controller.iterate(self)

		for n in self.nodes:
			n.iterate()

