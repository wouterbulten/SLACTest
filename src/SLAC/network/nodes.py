"""
@author Wouter Bulten
"""
import math
import numpy as np
from abc import ABCMeta, abstractmethod

class Node(object):
	"""Base Node

	Arguments:
		x: Current x position
		y: Current y position
	"""	

	__metaclass__ = ABCMeta
	
	def __init__(self, x = 0, y = 0):
		
		self.x = x
		self.y = y

	def initialize(self, x, y):
		"""Reset the state of the node"""
		self.x = x
		self.y = y
		
	@abstractmethod
	def iterate(self):
		pass

	def getPosition(self):
		"""Return the position of this node"""
		return (self.x, self.y)
	
	def setPosition(self, x, y):
		"""Set the position of a node"""
		self.x = x
		self.y = y
	
	def getDistance(self, x, y):
		"""Get the distance between this node and a specific point"""
		return math.sqrt(math.pow((x - self.x),2) + math.pow((y - self.y),2))

class MovingNode(Node):
	""" Node that moves
	
	Keeps track of all previous positions. Must be extended by
	implementing a move method.
	"""
	__metaclass__ = ABCMeta
	
	def __init__(self, x = 0, y = 0):
		Node.__init__(self, x, y)
		self.predX = x
		self.predY = y
		self.trace = [(x,y)]
		
	def initialize(self, x, y):
		self.trace = [(x,y)]
		Node.initialize(self, x, y)
		
	@abstractmethod
	def move(self):
		pass
	
	def moveToPosition(self, x, y):
		"""Move the node to a position"""
		self.trace.append((x, y))
		self.x = x
		self.y = y
	
class BouncingNode(MovingNode):
	""" Simple bouncing node within some box
	
	Arguments:
		x: Current x position
		y: Current y position
		maxX: Maximum size of x coordinate
		maxY: Maximum size of y coordinate

	Movement is based on:
		r: Rotation (radial)
		s: Speed
	"""	
	
	def __init__(self, maxX = 100, maxY = 100, x = 0, y = 0, ):
		MovingNode.__init__(self, x, y)

		self.maxX = maxX
		self.maxY = maxY
		self.r = 0
		self.s = 1
		
	def setMotion(self, angle, speed):
		self.r = angle
		self.s = speed

	def initialize(self, x, y):
		"""Set random movement"""
		MovingNode.initialize(self, x, y)
		
		r = (2 * np.random.random()) * math.pi
		s = (2 * np.random.random()) + 0.1
			
		self.setMotion(r, s)
		
	def iterate(self):
		self.move()
		
	def move(self):
		xn = max(min(self.x + math.cos(self.r) * self.s, self.maxX), 0)
		yn = max(min(self.y + math.sin(self.r) * self.s, self.maxY), 0)
		
		if xn == 0 or xn == self.maxX:
			self.r = math.pi - self.r
		elif yn == 0 or yn == self.maxY:
			self.r = 2 * math.pi - self.r
		
		self.moveToPosition(xn, yn)