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

sID = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
print("SLAC " + sID)
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
print("Saving Isomap prediction")
anim.save("sim_isomap_" + sID + ".mp4", writer="ffmpeg")

# Create GPLVM
gplvm = GPLVM(Y, 2, X = X)

print("Running optimization")
gplvm.optimize(messages=True)#, max_iters = 500, max_f_eval = 500)#, optimizer = 'scg')
predX, predY = zip(*gplvm.X)
predX = np.array(predX)
predY = np.array(predY)

# Create a animation
anim = PlaybackAnimation(nodes[:-1], user, predX, predY)
print("Saving GPLVM prediction")
anim.save("sim_optim_" + sID + ".mp4", writer="ffmpeg")