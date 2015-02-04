"""
@author Wouter Bulten
"""
import math
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
		self.predX = x
		self.predY = y
		self.r = 0
		self.s = 1
		self.trace = []
		self.predTrace = []

	@abstractmethod
	def move(self):
		pass

	def setPosition(self, x, y):
		self.trace.append((x, y))
		self.x = x
		self.y = y
		
	def setPrediction(self, x, y):
		self.predTrace.append((x, y))
		self.predX = x
		self.predY = y

	def getPosition(self):
		"""Return the position of this node"""
		return (self.x, self.y)
	
	def getPredictedPosition(self):
		return (self.predX, self.predY)

	def getDistance(self, x, y):
		"""Get the distance between this node and a specific point"""
		return math.sqrt(math.pow((x - self.x),2) + math.pow((y - self.y),2))

class BouncingNode(Node):
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
	
	def __init__(self, x = 0, y = 0, maxX = 100, maxY = 100):
		super().__init__(x, y)

		self.maxX = maxX
		self.maxY = maxY
		self.r = 0
		self.s = 1
		
	def setMotion(self, angle, speed):
		self.r = angle
		self.s = speed

	def move(self):
		xn = max(min(self.x + math.cos(self.r) * self.s, self.maxX), 0)
		yn = max(min(self.y + math.sin(self.r) * self.s, self.maxY), 0)
		
		if xn == 0 or xn == self.maxX:
			#self.r -= math.pi
			self.r = math.pi - self.r
		elif yn == 0 or yn == self.maxY:
			self.r = 2 * math.pi - self.r
		
		self.setPosition(xn, yn)