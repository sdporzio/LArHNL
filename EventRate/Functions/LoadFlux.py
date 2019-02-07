'''
Load up HNL flux for detector from .dat formatted file
'''
import os, sys, math
import numpy as np
import pandas as pd
# Perform traditional check of environment variable
def GetEnvVariable(varName):
    try:
        var = os.environ[varName]
        if var not in sys.path: sys.path.append(var)
        return var
    except KeyError:
        raise Exception("%s not found.\nPlease source setup.sh!" %varName)
basedir = GetEnvVariable('HNL_BASEDIR')

def LoadFlux(nuMass_gev):
	d = pd.read_csv(basedir+'/Data/Fluxes/MicroBooNE/sterileFlux_m%.3f_thetaMuOnly_NoDecayProb.dat' %nuMass_gev,sep=' ',header=None,names=['bins','total'])
	return d