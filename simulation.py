import network.nodes as nodes
import environment.world as world

config = {
	
	'nNodes':	5,
	'xMax':		50,
	'yMax':		50,
}

# Create a new world
world = world.World(config['xMax'], config['yMax'])

# Instantiate nodes with a random position
nodes = [nodes.Node(*world.getRandomPosition()) for x in range(0, config['nNodes'])]

print nodes[0]._x
print nodes[0]._y
print [node.getSignalStrengthAtLocation(50,50) for node in nodes]