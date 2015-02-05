'''
Created on Feb 4, 2015

@author: wouterbulten
'''


def predict(node, nodes):
    """ Predict position of node given nodes"""
    
    rssi = [n.getSignalStrengthAtLocation(*node.getPosition()) for n in nodes if n != node]
    
    #print(rssi)

class GPPredictor(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        