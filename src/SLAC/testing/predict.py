'''
Created on Feb 5, 2015

@author: wouterbulten
'''
import network.wireless as wsn
import environment.world as env
import simulation.controllers as contr
from predictor.probabilistic import predict
import numpy as np

config = {
    
    #'movingNodes':    1,
    'fixedNodes':    2,
    'xMax':        25,
    'yMax':        25,
}

# Create a new world
world = env.World(config['xMax'], config['yMax'])
# Instantiate nodes with a random position
nodes = [wsn.MovingAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['fixedNodes'])]
#nodes.extend([wsn.FixedAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['movingNodes'])])
user = wsn.MovingAP(maxX = world.getMaxX(), maxY = world.getMaxY())
nodes.append(user)

# Create a network controller, containing the world and nodes
controller = contr.NetworkController(world, nodes)
# Initialize the world, gives nodes initial speed and direction
controller.initialize()

X = np.array([n.getSignalStrengthAtLocation(*user.getPosition()) for n in nodes if n != user])

for i in range(0, 100):
    
    # Update the total network
    controller.iterate()
    
    # Get RSSI measurements
    rssi = [n.getSignalStrengthAtLocation(*user.getPosition()) for n in nodes if n != user]
    X = np.vstack((X, rssi))

print(X)
