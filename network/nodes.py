"""
@author Wouter Bulten
"""
import math

class Node(object):

	def __init__(self, x, y, txPower = -59, n = 2):

		self.x = x
		self.y = y
		self.txPower = txPower
		self.n = n #Signal propagation constant

	def getSignalStrengthAtLocation(self, x, y):
		return self.RSSI(self.getDistance(x,y))

	def getDistance(self, x, y):
		"""Get the distance between this node and a specific point"""
		return math.sqrt(math.pow((x - self.x),2) + math.pow((y - self.y),2))

	def RSSI(self, dist):
		"""Get the RSSI strength at a given distance"""
		return -(10 * self.n) *  math.log10(dist) + self.txPower