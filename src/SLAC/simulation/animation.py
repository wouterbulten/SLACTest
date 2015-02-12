'''
Created on Feb 4, 2015

@author: wouterbulten
'''
import matplotlib
from ..network.wireless import MovingAP
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

class PlaybackAnimation(animation.TimedAnimation):
    '''
    Animator object
    '''
    def __init__(self, nodes, user, Xpred, Ypred):
                      
        fig, (combAx, predAx) = plt.subplots(1, 2, squeeze=True, figsize=(24,10)  )

        self.nodesPlt, = combAx.plot([], [], 'ro')
        self.userPlt, = combAx.plot([], [], 'bo')
        self.predPlt, = predAx.plot([], [], 'wo')
        self.tracePlt, = combAx.plot([], [], 'b-')
        self.tracePredPlt, = predAx.plot([], [], 'k-')

        combAx.set_xlabel('X')
        combAx.set_ylabel('Y')
        combAx.set_xlim(0, 25)
        combAx.set_ylim(0, 25)
        
        predAx.set_xlabel('X')
        predAx.set_ylabel('Y')
        
        xLimMin = round(min(min(Xpred), min(Ypred)))
        xLimMax = round(max(max(Xpred), max(Ypred)))
        
        predAx.set_xlim(xLimMin, xLimMax)
        predAx.set_ylim(xLimMin, xLimMax)
                
        self.iteration = 0
        self.nodes = nodes
        self.user = user
        self.Xpred = Xpred
        self.Ypred = Ypred

        animation.TimedAnimation.__init__(self, fig, interval=100, blit=True, repeat=False, repeat_delay=500)
      
    def show(self):
        plt.show()
          
    def _draw_frame(self, iteration):

        # Plot the nodes
        x,y = zip(*[n.trace[iteration] if isinstance(n, MovingAP) else n.getPosition() for n in self.nodes])
        self.nodesPlt.set_data(x,y)
        
        # Plot the user
        x,y = self.user.trace[iteration]
        self.userPlt.set_data([x], [y])
        
        # Plot the user trace
        xTrace, yTrace = self.tracePlt.get_data()
        xTrace.append(x)
        yTrace.append(y)
        self.tracePlt.set_data(xTrace, yTrace)
        
        # Plot the prediction
        x = self.Xpred[iteration]
        y = self.Ypred[iteration]
        self.predPlt.set_data([x], [y])
        
        # Plot the predicted trace
        xTrace, yTrace = self.tracePredPlt.get_data()
        xTrace.append(x)
        yTrace.append(y)
        self.tracePredPlt.set_data(xTrace, yTrace)
                
        self._drawn_artists = [self.predPlt, 
            self.nodesPlt, self.userPlt, self.tracePlt, self.tracePredPlt]
        
    def _init_draw(self):
        self.nodesPlt.set_data([], [])
        self.userPlt.set_data([], [])
        self.predPlt.set_data([], [])
        self.tracePlt.set_data([], [])
        self.tracePredPlt.set_data([], [])
        
    def new_frame_seq(self):
        self.iteration = 0 #reset the iterations
        return iter(range(len(self.user.trace) - 2))
    
class NetworkAnimation(animation.TimedAnimation):
    """Animator to simultaneously animate and run a network"""
    
    def __init__(self, networkController, interval = 50, iterations = 100):
        fig = plt.figure()
        combAx = fig.add_subplot(1,1,1)
        self.nodesPlt, = plt.plot([], [], 'ro')
        self.predPlt, = plt.plot([], [], 'wo')

        combAx.add_line(self.nodesPlt)
        combAx.add_line(self.predPlt)
        combAx.set_xlabel('X')
        combAx.set_ylabel('Y')
        combAx.set_xlim(0, 25)
        combAx.set_ylim(0, 25)
        
        self.iteration = 0
        self.network = networkController

        animation.TimedAnimation.__init__(self, fig, interval=interval, blit=True)
      
    def show(self):
        plt.show()
          
    def _draw_frame(self, framedata):
 
        self.network.iterate();
        
        x,y = zip(*[n.getPosition() for n in self.network.nodes])
        xPred,yPred = zip(*[(50,50) for n in self.network.nodes])
        
        self.nodesPlt.set_data(x,y)
        self.predPlt.set_data(xPred,yPred)
        
        self._drawn_artists = [self.predPlt, self.nodesPlt]

    def _init_draw(self):
        self.nodesPlt.set_data([], [])
        self.predPlt.set_data([], [])
        
    def new_frame_seq(self):
        return iter(range(self.network.iteration + 1)) 