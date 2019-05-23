'''
Contains functions used to calculate kinematic and enhancement factors
to scale the different components of the original neutrino (numu/nue) flux
in order to obtain the heavy sterile neutrino flux
'''
# Perform traditional check of environment variable
import os, sys
def GetEnvVariable(varName):
    try:
        var = os.environ[varName]
        if var not in sys.path: sys.path.append(var)
        return var
    except KeyError:
        raise Exception("%s not found.\nPlease source setup.sh!" %varName)
basedir = GetEnvVariable('HNL_BASEDIR')
import numpy as np
import pandas as pd

# In GeV
# Load up constants
const = pd.read_json(basedir+'/GenerateFlux/Functions/constants.json')
mass = {
    'e': const['physics']['mass']['e']/1000.,
    'mu':  const['physics']['mass']['mu']/1000.,
    'tau': const['physics']['mass']['tau']/1000.,
    'nu_e': 1e-6,
    'nu_mu': 1e-6,
    'nu_tau': 1e-6,
    'K':  const['physics']['mass']['k+']/1000.,
    'K0':  const['physics']['mass']['k0']/1000.,
    'pi':  const['physics']['mass']['pi+']/1000.,
    'pi0':  const['physics']['mass']['pi0']/1000.
}

def fLambda(x,y,z):
    return pow(x,2.) + pow(y,2.) + pow(z,2.) - 2.*(x*y + y*z + x*z)
def fF(a,b):
    return a + b - pow((a-b),2.)
def fDelta(m,M):
    return pow(m,2.)/float(pow(M,2.))
def fRho(a,b):
    fl = fLambda(1,a,b)
    if fl < 0: return 0
    result = fF(a,b)*np.sqrt(fl)
    if result > 0: return result
    else: return 0
def kFactor(meson,lepton,nMass):
    '''
    Kinematic factor calculating the enhancement for each decay channel, depending on the masses of the mesons and leptons involved in the decay
    '''
    mMass = mass[meson]
    lMass = mass[lepton]
    num = fRho(fDelta(lMass,mMass),fDelta(nMass,mMass))
    den = fDelta(lMass,mMass) * np.power( 1.-fDelta(lMass,mMass) ,2.)
    return num/float(den)

# OTHER DUMMY FACTORS

def muonFactor(nMass):
    '''
    Dummy factor that switches off decay channels that involve a muon,
    when the mass of the HSN is larger than the energy available.
    '''
    if nMass<mass['mu']:
        return 1.
    else:
        return 0.

def k0Factor(lepton,nMass):
    '''
    Dummy factor that switches off decay channels that involve a K0,
    when the mass of the HSN is larger than the energy available.
    '''
    if nMass<(mass['K0']-mass[lepton]):
        return 1.
    else:
        return 0.

def incpiFactor(lepton,nMass):
    '''
    Dummy factor that switches off decay channels that involve a K decay including a pi0,
    when the mass of the HSN is larger than the energy available.
    '''
    if nMass<(mass['K']-mass['pi0']-mass[lepton]):
        return 1.
    else:
        return 0.

def otherFactor(nMass):
    '''
    Dummy factor that switches off other decay channels,
    when the mass of the HSN is larger than the energy available.
    Since I don't know what these channels are, I am assuming they switch off very early (at pi->mu N threshold).
    '''
    if nMass<(mass['pi']-mass['mu']):
        return 1.
    else:
        return 0.    