'''
Created on Feb 4, 2015

@author: wouterbulten
'''
import math
from network.nodes import Node, BouncingNode
from abc import ABCMeta, abstractmethod

def RSSI(self, dist, n, txPower):
    """Get the RSSI strength at a given distance"""
    return -(10 * n) *  math.log10(dist) + txPower
    
class WirelessEntity(metaclass=ABCMeta):
    """
    Wireless entity
    
    Arguments:
        x: Current x position
        y: Current y position
        txPower: Transmitting power at 1 m
        n: Signal propagation constant
    """
    
    def __init__(self, txPower = -59, n = 2):

        self.txPower = txPower
        self.n = n #Signal propagation constant
            
    @abstractmethod
    def getDistance(self, x, y):
        pass
    
    def getSignalStrengthAtLocation(self, x, y):
        """Return the signal strength of this node at a particular position"""
        return RSSI(self.getDistance(x,y), self.n, self.txPower)

class FixedAP(WirelessEntity, Node):
    """ Non-moving access point
    
    Builds upon a fixed node and on WirelessEntity
    for functionality regarding signal strength and such.
    """
    
    def __init__(self, maxX, maxY, txPower = -59, n = 2):
        WirelessEntity.__init__(self, txPower, n)
        Node.__init__(self)
        
    def iterate(self):
        pass
    
    def getDistance(self, x, y):
        Node.getDistance(self, x, y)  
        
class MovingAP(WirelessEntity, BouncingNode):
    """ Moving access point
    
    Builds upon a moving node (for the movement) and on WirelessEntity
    for functionality regarding signal strength and such.
    """
    
    def __init__(self, maxX, maxY, txPower = -59, n = 2):
        WirelessEntity.__init__(self, txPower, n)
        BouncingNode.__init__(self, maxX, maxY)
        
    def getDistance(self, x, y):
        BouncingNode.getDistance(self, x, y)