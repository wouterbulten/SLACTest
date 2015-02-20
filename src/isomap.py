'''
Created on Feb 20, 2015

@author: wouterbulten
'''
import matplotlib
matplotlib.use('TKAgg')
import numpy as np
from SLAC.simulation.animation import PlaybackAnimation
from GPy.models.gplvm import GPLVM
from matplotlib import pylab
import time
import datetime
from sklearn.manifold import Isomap

print("Loading data from file")

try:
    simData = np.load('simulation_data.npy').item()
    Y = simData['Y']
    user = simData['user']
    nodes = simData['nodes']
except IOError:
    print("ERROR: Missing data file. First run generateData.py to generate a data file.")
    exit()
    
    
# Create isomap object
map = Isomap()

X = map.fit_transform(Y)
predX, predY = zip(*X)

anim = PlaybackAnimation(nodes[:-1], user, predX, predY)