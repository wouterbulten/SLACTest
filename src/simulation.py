import network.nodes as nodes
import environment.world as env
import simulation.controllers as contr
import matplotlib
matplotlib.use('TKAgg')#, for blit=True
import matplotlib.pyplot as plt

config = {
	
	'nNodes':	50,
	'xMax':		100,
	'yMax':		100,
}

# Create a new world
world = env.World(config['xMax'], config['yMax'])

# Instantiate nodes with a random position
nodes = [nodes.BouncingNode(maxX = world.getMaxX(), maxY = world.getMaxY()) for x in range(0, config['nNodes'])]

controller = contr.NetworkController(world, nodes)

controller.initialize()

for i in range(0, 300):
	controller.iterate()
	
fig = plt.figure()

for n in controller.nodes:
	x,y = zip(*n.trace)
	plt.plot(x,y)

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()