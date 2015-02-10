'''
Created on Feb 5, 2015

@author: wouterbulten
'''
import matplotlib
matplotlib.use('TKAgg')
import SLAC.network.wireless as wsn
import SLAC.environment.world as env
import SLAC.simulation.controllers as contr
import numpy as np
from SLAC.simulation.animation import PlaybackAnimation
from GPy.models.gplvm import GPLVM
from matplotlib import pylab

config = {
    
    #'movingNodes':    1,
    'fixedNodes':    100,
    'xMax':        25,
    'yMax':        25,
}

# Create a new world
world = env.World(config['xMax'], config['yMax'])
# Instantiate nodes with a random position
nodes = [wsn.FixedAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['fixedNodes'])]

#nodes.extend([wsn.FixedAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['movingNodes'])])
user = wsn.MovingAP(maxX = world.getMaxX(), maxY = world.getMaxY())
nodes.append(user)

# Create a network controller, containing the world and nodes
controller = contr.NetworkController(world, nodes, False)
# Initialize the world, gives nodes initial speed and direction
controller.initialize()

Y = np.array([n.getSignalStrengthAtLocation(*user.getPosition(), noise=0) for n in nodes if n != user])

# Simulate movement in the network
print("Simulating movement")
for i in range(0, 1000):
    
    # Update the total network
    controller.iterate()
    
    # Get RSSI measurements
    rssi = [n.getSignalStrengthAtLocation(*user.getPosition(), noise=0) for n in nodes if n != user]
    Y = np.vstack((Y, rssi))


predX, predY = zip(*user.trace)
predX = np.array(predX) + np.random.rand()
predY = np.array(predY) + np.random.rand()

# Create a animation
anim = PlaybackAnimation(nodes[:-1], user, predX, predY)
if matplotlib.is_interactive():
    pylab.ioff()
    
anim.show()
