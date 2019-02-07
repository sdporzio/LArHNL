import sys,os, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, colors

def MakeEventMat2dHist(massRange,thetaRange,eventMat,filename='out',eventsForDiscovery=3):
	# Make event rate plot
	clim = (eventsForDiscovery,1e8)
	cmap = plt.cm.autumn_r
	levels = [eventsForDiscovery,eventsForDiscovery+1]
	# Clear eventMat (remove events < 3)
	eventMat[eventMat<eventsForDiscovery] = 0.

	# Draw 2d histo for MicroBooNE
	plt.figure(figsize=(10,10))
	plt.pcolormesh(massRange, thetaRange, eventMat, cmap=cmap, norm=colors.LogNorm(clim))
	plt.yscale('log')
	plt.xlabel(r'$M_N$ [MeV/$c^2$]',fontsize=18)
	plt.ylabel(r'$|\Theta_{\mu}|^2$',fontsize=18)
	plt.tick_params(axis='both', which='major', labelsize=15)
	plt.tick_params(axis='both', which='minor', labelsize=8)
	plt.ylim((5e-9,1e-4))
	plt.xlim((0.22,0.41))
	plt.clim(clim)
	plt.colorbar()
	plt.savefig('Plots/%s.pdf' %filename,bbox_inches='tight', pad_inches=0.1)
	plt.show()