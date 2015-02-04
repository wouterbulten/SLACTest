"""
@author Wouter Bulten
"""

import numpy as np

class World(object):

	def __init__(self, dimX, dimY):

		self.dimX = dimX
		self.dimY = dimY

	def getRandomPosition(self):
		return [np.random.rand() * self.dimX, np.random.rand() * self.dimY]
