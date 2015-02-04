'''
Created on Feb 4, 2015

@author: wouterbulten
'''
from network.nodes import BouncingNode
import math

def RSSI(self, dist, n, txPower):
    """Get the RSSI strength at a given distance"""
    return -(10 * n) *  math.log10(dist) + txPower
    
class WirelessNode(BouncingNode):
    """
    Wireless node
    
    Arguments:
        x: Current x position
        y: Current y position
        maxX: Maximum size of x coordinate
        maxY: Maximum size of y coordinate
        txPower: Transmitting power at 1 m
        n: Signal propagation constant
    """

    def __init__(self, x = 0, y = 0, maxX = 100, maxY = 100, txPower = -59, n = 2):
        super().__init__(x, y, maxX, maxY)
        self.txPower = txPower
        self.n = n #Signal propagation constant
        
            
    def getSignalStrengthAtLocation(self, x, y):
        """Return the signal strength of this node at a particular position"""
        return RSSI(self.getDistance(x,y), self.n, self.txPower)