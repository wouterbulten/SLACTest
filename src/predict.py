'''
Created on Feb 5, 2015

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

sID = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
print("SLAC " + sID)
print("Loading data from file")

try:
    simData = np.load('simulation_data.npy').item()
    Y = simData['Y']
    user = simData['user']
    nodes = simData['nodes']
except IOError:
    print("ERROR: First run generateData.py to generate a data file")
    exit()
    
# Create GPLVM
print("Init PCA")
gplvm = GPLVM(Y, 2, init='PCA')

predX, predY = zip(*gplvm.X)
predX = np.array(predX)
predY = np.array(predY)

# Create a animation
anim = PlaybackAnimation(nodes[:-1], user, predX, predY)
print("Saving PCA animation")
anim.save("sim_init_" + sID + ".mp4", writer="ffmpeg")

print("Running optimization")
gplvm.optimize(messages=True)#, max_iters = 500, max_f_eval = 500)#, optimizer = 'scg')
predX, predY = zip(*gplvm.X)
predX = np.array(predX)
predY = np.array(predY)

# Create a animation
anim = PlaybackAnimation(nodes[:-1], user, predX, predY)
print("Saving GPLVM prediction")
anim.save("sim_optim_" + sID + ".mp4", writer="ffmpeg")