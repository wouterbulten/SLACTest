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
import SLAC.predictor.gplvm as gplvm
from SLAC.simulation.animation import PlaybackAnimation

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
controller = contr.NetworkController(world, nodes)
# Initialize the world, gives nodes initial speed and direction
controller.initialize()

Y = np.array([n.getSignalStrengthAtLocation(*user.getPosition(), noise=0) for n in nodes if n != user])

# Simulate movement in the network
for i in range(0, 100):
    
    # Update the total network
    controller.iterate()
    
    # Get RSSI measurements
    rssi = [n.getSignalStrengthAtLocation(*user.getPosition(), noise=0) for n in nodes if n != user]
    Y = np.vstack((Y, rssi))


gpLVM = gplvm.GPLVM(Y,2)
gpLVM.learn(1)

predX, predY = zip(*gpLVM.gp.X)

# Move the prediction to the starting point of the user (for the animation, does not change the accuracy)
predX = np.array(predX) + user.trace[0][0]
predY = np.array(predY) + user.trace[0][1]
print(predX)
print(predY)
print(user.trace[0])

# Create a animation
anim = PlaybackAnimation(nodes[:-1], user, predX, predY)
anim.show()