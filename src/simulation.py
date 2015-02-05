import network.wireless as wsn
import environment.world as env
import simulation.controllers as contr
import simulation.animation as anim

config = {
	
	'nNodes':	50,
	'xMax':		100,
	'yMax':		100,
}

# Create a new world
world = env.World(config['xMax'], config['yMax'])
# Instantiate nodes with a random position
nodes = [wsn.MovingAP(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['nNodes'])]
# Create a network controller, containing the world and nodes
controller = contr.NetworkController(world, nodes)
# Initialize the world, gives nodes initial speed and direction
controller.initialize()

# Create a controller for the visualization
animation = anim.NetworkAnimation(controller)
# Start
animation.show()