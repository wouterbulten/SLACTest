"""
@author Wouter Bulten
"""

import numpy as np

class World:

	def __init__(self, dimX, dimY):

		self._dimX = dimX
		self._dimY = dimY

	def getRandomPosition(self):
		return [np.random.rand() * self._dimX, np.random.rand() * self._dimY]
