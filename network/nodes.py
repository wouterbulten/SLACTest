"""
@author Wouter Bulten
"""
import math

class Node:

	def __init__(self, x, y, txPower = -59, n = 2):

		self._x = x
		self._y = y
		self._txPower = txPower
		self._n = 2 #Signal propagation constant

	def getSignalStrengthAtLocation(self, x, y):
		return self.RSSI(self.getDistance(x,y))

	def getDistance(self, x, y):
		"""Get the distance between this node and a specific point"""
		return math.sqrt(math.pow((x - self._x),2) + math.pow((y - self._y),2))

	def RSSI(self, dist):
		"""Get the RSSI strength at a given distance"""
		return -(10 * self._n) *  math.log10(dist) + self._txPower