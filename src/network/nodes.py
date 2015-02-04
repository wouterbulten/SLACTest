"""
@author Wouter Bulten
"""
import math
from abc import ABCMeta, abstractmethod

class Node(object):
	"""Base Node

	Attributes:
		x: Current x position
		y: Current y position
		txPower: Transmitting power at 1 m
		n: Signal propagation constant
	"""	

	__metaclass__ = ABCMeta

	def __init__(self, x, y, maxX, maxY, txPower = -59, n = 2):

		self.x = x
		self.y = y
		self.maxX = maxX
		self.maxY = maxY
		self.r = 0
		self.s = 1
		self.txPower = txPower
		self.n = n #Signal propagation constant

	@abstractmethod
	def move(self):
		pass

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	def getSignalStrengthAtLocation(self, x, y):
		return self.RSSI(self.getDistance(x,y))

	def getDistance(self, x, y):
		"""Get the distance between this node and a specific point"""
		return math.sqrt(math.pow((x - self.x),2) + math.pow((y - self.y),2))

	def RSSI(self, dist):
		"""Get the RSSI strength at a given distance"""
		return -(10 * self.n) *  math.log10(dist) + self.txPower

class BouncingNode(Node):
	""" Simple bouncing node within some box
	
	Attributes:
		maxX: Maximum size of x coordinate
		maxY: Maximum size of y coordinate
		r: Rotation (radial)
		s: Speed
	"""	
	
	def __init__(self, x, y, maxX, maxY, txPower = -59, n = 2):
		super().__init__(x, y, txPower, n)

		self.maxX = maxX
		self.maxY = maxY
		self.r = 0
		self.s = 1
		
	def setMotion(self, angle, speed):
		self.r = angle
		self.s = speed

	def move(self):
		xn = self.x + math.cos(self.r) * self.s
		yn = self.y + math.sin(self.r) * self.s
		
		if xn > self.maxX:
			xn = self.maxX;
			bounce = True;
		if yn > self.maxY:
			yn = self.maxY
			bounce = True;
		if xn < 0:
			xn = 0;
			bounce = True;
		if yn < 0:
			yn = 0	
			bounce = True;
		
		if bounce:
			if self.r >= math.pi:
				self.r -= math.pi
			else:
				self.r += math.pi
		
		self.setPosition(xn, yn)