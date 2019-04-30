'''
Determine event rate of decayed HNL observed at MicroBooNE, given a mass value, POT number, mixing angle and detector.
Event rate calculated using same convention as Asaka et al., page 11-12 (https://arxiv.org/pdf/1212.1062.pdf)
For more informations, see directory _Formulas
'''
import os, sys, math
import numpy as np
import pandas as pd
import Functions.DecayLength as DL
import Functions.LoadFlux as LF
# Perform traditional check of environment variable
def GetEnvVariable(varName):
    try:
        var = os.environ[varName]
        if var not in sys.path: sys.path.append(var)
        return var
    except KeyError:
        raise Exception("%s not found.\nPlease source setup.sh!" %varName)
basedir = GetEnvVariable('HNL_BASEDIR')

# Load up constants
const = pd.read_json(basedir+'/Data/Constants/constants.json')
gFermi = const['physics']['constants']['Gf'] # 1/MeV^2
hbar = const['physics']['constants']['hbar'] # MeV*seconds
c = const['physics']['constants']['c'] # m/seconds
eMass = const['physics']['mass']['e'] # Mev/c^2
muMass =  const['physics']['mass']['mu'] # Mev/c^2
piMass = const['physics']['mass']['pi+'] # Mev/c^2
piV = const['physics']['ckm']['ud']
piF = const['physics']['decay_const']['pi+'] # MeV

### Return event rate for detector, given mass (in GeV), pot, detector and mixing angle
def EventRate_MuPi(nuMass,theta_mu2,POT,detector):
    # Physics parameters
    nuMass_gev = nuMass # GeV
    nuMass_mev = nuMass_gev*1000.
    muMass =  const['physics']['mass']['mu'] # Mev/c^2
    piMass = const['physics']['mass']['pi+'] # Mev/c^2
    kMass = const['physics']['mass']['k+'] # Mev/c^2

    # Detector parameters
    distance = const['experiment'][detector]['distance'] # m
    volume = const['experiment'][detector]['fiducial_volume'] # m

    # Generate hsn flux
    flux = LF.LoadFlux(nuMass_gev)

    # Perform transformation.
    # Fluxes by internal flux generator are usually in y:nu/POT/GeV/cm2 and x:GeV
    # and the pre-generated fluxes have a nominal theta_mu2 = 1
    # We want y:nu/POT/MeV/m2 (x10) and x:MeV (x1000) and scaled by correct mixing angle
    for i in range(len(flux['bins'])):
        flux['bins'][i] = flux['bins'][i]*1000
        flux['total'][i] = flux['total'][i]*10*theta_mu2

    rate = [[],[]] # Heavy neutral lepton rate spectrum as a function of energy
    for i in range(len(flux['bins'])):
        # Decay length gets broken if it gets unphysical values (e.g. total energy less than mass)
        if nuMass_mev<=piMass+muMass or flux['bins'][i]<=nuMass_mev: calcRate = 0.
        else:
            calcRate = volume*POT*flux['total'][i]/DL.Length_Nu2MuPi(nuMass_mev,theta_mu2,flux['bins'][i])
        rate[0].append(flux['bins'][i])
        rate[1].append(calcRate)

    totalRate = 0.
    for i in range(len(rate[0])):
        # Get the bin width for integration, usually same size but you never know
        if i!=len(flux['bins'])-1: deltaE = flux['bins'][i+1]-flux['bins'][i]
        else: deltaE = flux['bins'][i]-flux['bins'][i-1]
        totalRate += rate[1][i]*deltaE

    return totalRate, rate[0], rate[1]