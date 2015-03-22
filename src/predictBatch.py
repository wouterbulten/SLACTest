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
import matplotlib.pyplot as plt

sID = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
print("SLAC " + sID)
print("Loading data from file")

try:
    simData = np.load('simulation_data.npy').item()
    Yraw = simData['Y']
    user = simData['user']
    nodes = simData['nodes']
except IOError:
    print("ERROR: Missing data file. First run generateData.py to generate a data file.")
    exit()
    
fixedNodes = nodes[0:100]
nodesX, nodesY = zip(*[n.getPosition() for n in fixedNodes])
userX, userY = zip(*user.trace)

plt.figure()
plt.ylabel('Y')
plt.xlabel('X')
plt.plot(nodesX, nodesY, 'ro');
plt.plot(userX, userY, 'b-');
plt.savefig('userPattern.pdf', format='pdf')
plt.show();

sds = [0, 1, 5, 10, 15];
plt.figure(figsize=(15, 25))
for (i, sd) in enumerate(sds):
    
    if(sd > 0):
        Y = np.array([[y + np.random.normal(0, sd) for y in z] for z in Yraw])
    else:
        Y = np.array([[y for y in z] for z in Yraw])
         
    # Create GPLVM
    print("Init PCA")
    gplvm = GPLVM(Y, 2, init='PCA')
    
    predX, predY = zip(*gplvm.X)
    predX = np.array(predX)
    predY = np.array(predY)
         
    ax = plt.subplot(len(sds), 2, (i*2)+1)
    plt.plot(predX, predY, 'k-')
    ax.set_title('PCA (noise=' + str(sd) + ')');

    print("Running optimization")
    gplvm.optimize(messages=True, max_iters = 1000, max_f_eval = 1000)#, optimizer = 'scg')
    predX, predY = zip(*gplvm.X)
    predX = np.array(predX)
    predY = np.array(predY)
    
    ax = plt.subplot(len(sds), 2, (i*2)+2)
    plt.plot(predX, predY, 'k-')
    ax.set_title('GP-LVM (noise=' + str(sd) + ')');

plt.tight_layout()
plt.ylabel('Y')
plt.xlabel('X')
plt.savefig('predictBatch.pdf', format='pdf')
plt.show();
