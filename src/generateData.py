'''
Created on Feb 11, 2015

@author: wouterbulten

Only generates data and saves it to a file

'''
import matplotlib
matplotlib.use('TKAgg')
import SLAC.simulation.controllers as contr
import numpy as np

Y, user, nodes = contr.generateData(25, 25, 50, 0, 500)

data = {'Y': Y, 'user': user, 'nodes': nodes}

np.save('simulation_data.npy', data)

print("Data saved")