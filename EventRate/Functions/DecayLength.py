'''
Calculate decay length given mass, mixing angle and neutrino energy
Decay length from Atre et al., page 48 (https://arxiv.org/pdf/0901.3589.pdf)
For more information, see directory 'Formulas'.
Mass and energy MUST BE in MeV
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

### Return decay length in meters, given mass and energy in MeV
def Length_Nu2MuPi(nuMass,theta_mu2,nuEnergy):
    # Define parameters involved
    nuMass = float(nuMass)
    nuEnergy = float(nuEnergy)
    hMass = float(piMass)
    lMass = float(muMass)
    hV = float(piV)
    hF = float(piF)

    # Calculate kinematics of HNL
    nuMomentum = math.sqrt(pow(nuEnergy,2)-pow(nuMass,2))
    gamma = nuEnergy/float(nuMass)
    beta = nuMomentum/float(nuEnergy)

    # Detemine terms of decay width
    lMass_scaled = p2(lMass)/float(p2(nuMass))
    hMass_scaled = p2(hMass)/float(p2(nuMass))
    i1 = I1_factor(lMass_scaled,hMass_scaled)

    mupi_width = p2(gFermi)/(16.*math.pi) * p2(hF) * p2(hV) * theta_mu2 * pow(nuMass,3) * i1
    mupi_width = 2. * mupi_width # For Majorana neutrino, charge conjugate processes also available, hence factor 2

    # Convert width to length
    lifetime = hbar/mupi_width
    length = beta*gamma*c*lifetime

    return length # m


### Auxiliary functions
def p2(x):
    return pow(x,2.)

def sq(x):
    return math.sqrt(x)

def lambda_factor(x,y,z):
    return p2(x) + p2(y) + p2(z) - 2*(x*y + y*z + x*z)

def I1_factor(x,y):
    return ((1 + x - y)*(1 + x) - 4*x) * sq(lambda_factor(1,x,y))