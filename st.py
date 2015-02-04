import network.nodes as nodes

import numpy as np
import matplotlib
matplotlib.use('TKAgg')#, for blit=True
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools

config = { 
	'nNodes': 	10,
	'nDims':	2,
	'xMax':		100,
	'yMax':		100,

	'movement': 1,

	'xLabel': 'X Position',
	'yLabel': 'Y Position',

	'nodeLayout': 'ro',
	'nodePredLayout': 'wo',
	'linkLayout': 'g-'
}

# Create random initial positions for nodes
startPositions = np.random.rand(config['nDims'], config['nNodes'])
startPositionsPrediction = np.random.rand(config['nDims'], config['nNodes'])

startPositions[0, :] = startPositions[0, :] * config['xMax']
startPositions[1, :] = startPositions[1, :] * config['yMax']
startPositionsPrediction[0, :] = startPositionsPrediction[0, :] * config['xMax']
startPositionsPrediction[1, :] = startPositionsPrediction[1, :] * config['yMax']

movementNodes = config['movement'] * (np.random.rand(config['nDims'], config['nNodes']) - 0.5)	

positionNodes = startPositions
positionPredictions = startPositionsPrediction

def moveNodes(positions):

	positions = positions + movementNodes

	for i in range(0, np.size(positions, 1)):
		
		if positions[0, i] > config['xMax']:
			positions[0, i] = config['xMax']
			movementNodes[0, i] = - movementNodes[0, i]

		if positions[1, i] > config['yMax']:
			positions[1, i] = config['yMax']
			movementNodes[1, i] = - movementNodes[1, i]

		if positions[0, i] < 0:
			positions[0, i] = 0
			movementNodes[0, i] = - movementNodes[0, i]

		if positions[1, i] < 0:
			positions[1, i] = 0
			movementNodes[1, i] = - movementNodes[1, i]

	return positions

def setLinkLines(nodes, predictions):

	for i in range(0, np.size(linkPlots, 0)):
		linkPlots[i].set_data([nodes[0, i], predictions[0, i]], [nodes[1, i], predictions[1, i]])

def init():
    return [gtPlot, predPlot] + linkPlots

def update_line(i):

	global positionPredictions, positionNodes
	if i == 0:
		return [gtPlot, predPlot] + linkPlots

	positionNodes = moveNodes(positionNodes)
	positionPredictions = positionPredictions

	gtPlot.set_data(positionNodes)
	predPlot.set_data(positionPredictions)

	setLinkLines(positionNodes, positionPredictions)
	
	return [gtPlot, predPlot] + linkPlots

fig = plt.figure()

gtPlot, = plt.plot([], [], config['nodeLayout']) #startPositions[0, :], startPositions[1, :]
predPlot, = plt.plot([], [], config['nodePredLayout']) #startPositionsPrediction[0, :], startPositionsPrediction[1, :],

linkPlots = [plt.plot([], [], config['linkLayout'])[0] for x in range(0, config['nNodes'])]

plt.xlim(0, config['xMax'])
plt.ylim(0, config['yMax'])
plt.xlabel(config['xLabel'])
plt.ylabel(config['yLabel'])

plt.title('')
simulation = animation.FuncAnimation(fig, update_line, 50, init_func=init, interval=25, blit=True)
#line_ani.save('lines.mp4')

plt.grid(True)
plt.show()