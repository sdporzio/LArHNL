import sys,os, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
# Perform traditional check of environment variable
def GetEnvVariable(varName):
    try:
        var = os.environ[varName]
        if var not in sys.path: sys.path.append(var)
        return var
    except KeyError:
        raise Exception("%s not found.\nPlease source setup.sh!" %varName)
basedir = GetEnvVariable('HNL_BASEDIR')
import EventRate.Functions.EventRates as ER
import Functions.eventMatHistogram as EMH

def LoopProgress(i,n):
	sys.stdout.write("\rProgress: %i%%" %((float(i)/float(n))*100))
	sys.stdout.flush()

### SETTINGS
POT = 2.0e20 # protons on target, three years livetime [uBooNE proposal]
nBins = 100
detector = 'microboone'
thetaRange = np.logspace(-10,-4,nBins) 
massRange = np.linspace(0.225,0.4,nBins)
eventsForDiscovery = 3


# Initialize event matrix
eventMat = np.empty((nBins, nBins))
# Fill event matrix
print "Filling event rate matrix..."
for j,mass in enumerate(massRange):
	LoopProgress(j+1,len(massRange))
	events, _, _ = ER.EventRate_MuPi(mass,1.,POT,detector) # Use nominal mixing angle 1
	for i,theta_mu2 in enumerate(thetaRange):
		eventMat[i,j] = events * np.power(theta_mu2,2.) # Event number scales with mixing angle (speeds up)
print "\r\033[KCompleted."

EMH.MakeEventMat2dHist(massRange,thetaRange,eventMat,'numberOfEvents',3)