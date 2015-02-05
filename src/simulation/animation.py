'''
Created on Feb 4, 2015

@author: wouterbulten
'''
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

class NetworkAnimation(animation.TimedAnimation):
    '''
    Animator object
    '''

    def __init__(self, networkController, interval = 50, iterations = 100):
        
        self.network = networkController
                
        fig = plt.figure()
        combAx = fig.add_subplot(1,1,1)
        #nodesAx = fig.add_subplot(1,2,2)
        #predAx = fig.add_subplot(1, 3, 3)

        self.nodesPlt, = plt.plot([], [], 'ro')
        self.predPlt, = plt.plot([], [], 'wo')

        combAx.add_line(self.nodesPlt)
        combAx.add_line(self.predPlt)
        combAx.set_xlabel('X')
        combAx.set_ylabel('Y')
        combAx.set_xlim(0, 100)
        combAx.set_ylim(0, 100)
        
        #nodesAx.add_line(self.predPlt)
        #nodesAx.set_xlabel('X')
        #nodesAx.set_ylabel('Y')
        #nodesAx.set_xlim(0, 100)
        #nodesAx.set_ylim(0, 100)
        
        #predAx.add_line(self.predPlt)
        #predAx.set_xlabel('X')
        #predAx.set_ylabel('Y')
        #predAx.set_xlim(0, 100)
        #predAx.set_ylim(0, 100)
        
        
        super().__init__(fig, interval=interval, blit=True)
      
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