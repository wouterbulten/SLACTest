'''
Created on Feb 5, 2015

@author: jameshensman
@author: wouterbulten (modification)

https://github.com/jameshensman/pythonGPLVM
'''
import numpy as np
import pylab
import predictor.pca as pca
import predictor.kernels as kernels
import predictor.gp as gp
from scipy import optimize


class GPLVM:
	""" TODO: this should inherrit a GP, not contain an instance of it..."""
	def __init__(self,Y,dim):
		self.Xdim = dim
		self.N,self.Ydim = Y.shape
		
		"""Use PCA to initalise the problem. Uses EM version in this case..."""
		myPCA_EM = pca.PCA_EM(Y,dim)
		myPCA_EM.learn(100)
		X = np.array(myPCA_EM.m_Z)
		
		self.gp = gp.GP(X,Y)#choose particular kernel here if so desired.
	
	def learn(self,niters):
		for i in range(niters):
			self.optimise_latents()
			self.optimise_GP_kernel()
			
	def optimise_GP_kernel(self):
		"""optimisation of the GP's kernel parameters"""
		self.gp.find_kernel_params()
		print(self.gp.marginal(), 0.5*np.sum(np.square(self.gp.X)))
	
	def ll(self,xx,i):
		"""The log likelihood function - used when changing the ith latent variable to xx"""
		self.gp.X[i] = xx
		self.gp.update()
		return -self.gp.marginal()+ 0.5*np.sum(np.square(xx))
	
	def ll_grad(self,xx,i):
		"""the gradient of the likelihood function for us in optimisation"""
		self.gp.X[i] = xx
		self.gp.update()
		self.gp.update_grad()
		matrix_grads = [self.gp.kernel.gradients_wrt_data(self.gp.X,i,jj) for jj in range(self.gp.Xdim)]
		grads = [-0.5*np.trace(np.dot(self.gp.alphalphK,e)) for e in matrix_grads]
		return np.array(grads) + xx
		
	def optimise_latents(self):
		"""Direct optimisation of the latents variables."""
		xtemp = np.zeros(self.gp.X.shape)
		for i,yy in enumerate(self.gp.Y):
			original_x = self.gp.X[i].copy()
			#xopt = optimize.fmin(self.ll,self.gp.X[i],disp=True,args=(i,))
			xopt = optimize.fmin_cg(self.ll,self.gp.X[i],fprime=self.ll_grad,disp=True,args=(i,))
			self.gp.X[i] = original_x
			xtemp[i] = xopt
		self.gp.X = xtemp.copy()
		
		
		
