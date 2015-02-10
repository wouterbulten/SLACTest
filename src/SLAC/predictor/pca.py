'''
Created on Feb 5, 2015

@author: jameshensman
@author: wouterbulten (modification)

https://github.com/jameshensman/pythonGPLVM
'''

import numpy as np
from scipy import linalg

class PCA_EM:
    def __init__(self,data,target_dim):
        """Maximum likelihood PCA by the EM algorithm"""
        self.X = np.array(data)
        self.N,self.d = self.X.shape
        self.q = target_dim
    def learn(self,niters):
        self.mu = self.X.mean(0).reshape(self.d,1)#ML solution for mu
        self.X2 = self.X - self.mu.T
        self.xxTsum = np.sum([np.dot(x,x.T) for x in self.X2])#precalculate for speed
        #initialise paramters:
        self.W = np.random.randn(self.d,self.q)
        self.sigma2 = 1.2
        for i in range(niters):
            #print self.sigma2
            self.E_step()
            self.M_step()

    def E_step(self):
        M = np.dot(self.W.T,self.W) + np.eye(self.q)*self.sigma2
        M_chol = linalg.cholesky(M)
        M_inv = linalg.cho_solve((M_chol,1),np.eye(self.q))
        self.m_Z = linalg.cho_solve((M_chol,1),np.dot(self.W.T,self.X2.T)).T
        self.S_z = M_inv*self.sigma2
        
    def M_step(self):
        zzT = np.dot(self.m_Z.T,self.m_Z) + self.N*self.S_z
        zzT_chol = linalg.cholesky(zzT)
        self.W = linalg.cho_solve((zzT_chol,0),np.dot(self.m_Z.T,self.X2)).T
        WTW = np.dot(self.W.T,self.W)
        self.sigma2 = self.xxTsum - 2*np.sum(np.dot(self.m_Z,self.W.T)*self.X2) + np.trace(np.dot(zzT,WTW))
        self.sigma2 /= self.N*self.d