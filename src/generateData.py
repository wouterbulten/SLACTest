'''
Created on Feb 11, 2015

@author: wouterbulten

Only generates data and saves it to a file

'''
import matplotlib
matplotlib.use('TKAgg')
import SLAC.simulation.controllers as contr
import numpy as np

Y, user = contr.generateData(25, 25, 25, 2, 500)

np.save('simulation_data', {'Y': Y, 'user': user})

print("Data saved")