import SLAC.network.wireless as wsn
import SLAC.environment.world as env
import SLAC.simulation.controllers as contr
import SLAC.simulation.animation as anim
import numpy as np

config = {
	
	#'movingNodes':	1,
	'fixedNodes':	10,
	'xMax':		25,
	'yMax':		25,
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

# Create a controller for the visualization
animation = anim.NetworkAnimation(controller)
# Start
animation.show()

#import time
#import datetime
#st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
#animation.save("sim_" + st + ".mp4", writer="ffmpeg")