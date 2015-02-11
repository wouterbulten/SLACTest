'''
Created on Feb 4, 2015

@author: wouterbulten
'''
import math
from SLAC.network.nodes import Node, BouncingNode
from abc import ABCMeta, abstractmethod
import numpy as  np

def RSSIraw(dist, n, txPower):
    """Get the RSSI strength at a given distance"""
    return -(10 * n) *  math.log10(dist) + txPower

def RSSI(dist, n, txPower, sd = 1):
    """RSSI with gaussian noise N(0,sd)"""
    return RSSIraw(dist, n, txPower) + np.random.normal(0, n)

def plotAccessPoint(node, xDim, yDim, precission):
    """Plot the signal strength of an access point"""
    from mpl_toolkits.mplot3d import Axes3D  # @UnresolvedImport
    from mpl_toolkits.mplot3d import axes3d  # @UnresolvedImport
    from matplotlib import cm
    import matplotlib.pyplot as plt
    
    X = np.linspace(0, xDim, precission)
    Y = np.linspace(0, yDim, precission)
    Z = np.array([node.getSignalStrengthAtLocation(x,y) for x in X for y in Y]).reshape(precission, precission)
    X,Y = np.meshgrid(X,Y, indexing='ij')
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap=cm.coolwarm,  # @UndefinedVariable
            linewidth=0, antialiased=True)
    
    plt.show()

def plotAPStrengthFromTrace(trace, node):
    """Plot the signal strength of an access point given a trace"""
    from mpl_toolkits.mplot3d import Axes3D  # @UnresolvedImport
    from mpl_toolkits.mplot3d import axes3d  # @UnresolvedImport
    from matplotlib import cm
    import matplotlib.pyplot as plt
    
    X, Y = zip(*trace)
    
    Z = np.array([node.getSignalStrengthAtLocation(*t) for t in trace])
    X,Y = np.meshgrid(X,Y, indexing='ij')
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm) # @UndefinedVariable
    
    plt.show()  
    
class WirelessEntity():
    """
    Wireless entity
    
    Arguments:
        txPower: Transmitting power at 1 m
        n: Signal propagation constant
    """
    
    __metaclass__ = ABCMeta
    
    def __init__(self, txPower = -59, n = 2):

        self.txPower = txPower
        self.n = n #Signal propagation constant
            
    @abstractmethod
    def getDistance(self, x, y):
        pass
    
    def getSignalStrengthAtLocation(self, x, y, noise = 1):
        """Return the signal strength of this node at a particular position"""
        return RSSI(self.getDistance(x,y), self.n, self.txPower, noise)

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
        return Node.getDistance(self, x, y)  
        
class MovingAP(WirelessEntity, BouncingNode):
    """ Moving access point
    
    Builds upon a moving node (for the movement) and on WirelessEntity
    for functionality regarding signal strength and such.
    """
    
    def __init__(self, maxX, maxY, txPower = -59, n = 2):
        WirelessEntity.__init__(self, txPower, n)
        BouncingNode.__init__(self, maxX, maxY)
        
    def getDistance(self, x, y):
        return BouncingNode.getDistance(self, x, y)