import network.nodes as nodes
import environment.world as world

config = {
	
	'nNodes':	5,
	'xMax':		100,
	'yMax':		100,
}

world = world.World(config['xMax'], config['yMax'])

nodes = [nodes.Node(*world.getRandomPosition()) for x in range(0, config['nNodes'])]

print nodes