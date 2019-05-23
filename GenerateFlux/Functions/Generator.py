'''
Contains functions loading the different components of the original neutrino (numu/nue) flux
and scaling them differently according to the mixing angle and masses value inputted
in order to obtain the heavy sterile neutrino flux
'''
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
import GenerateFlux.Functions.Kinematics as K

# Input/Output functions
def FromPickle(filename):
    return pickle.load(open(filename,'rb'),encoding='bytes')
def ToPickle(data,filename):
    pickle.dump(data, open(filename,'wb'))

# Physics functions
def GenerateSterileFlux(nMass=0.0001,theta_e2=1,theta_mu2=1,applyDecayProb=False):
    '''
    Given mass value and mixing angles, return heavy sterile neutrino flux
    correctly scaled. A decay probability factor (proportional to inverse of momentum)
    can be applied to obtain shape of flux of hsn DECAYING inside the detector.
    However, this is only a factor to obtain correct shape and will mess up with normalization,
    DON'T use if you plan on getting absolute numbers out of distributions
    (use it only to draw random MC from it, for example)
    '''
    # Load data
    data = pd.read_pickle(basedir+'/GenerateFlux/InputFlux/flux.pkl')
    df = dict()
    df['bins'] = data['bins']

    # Apply decay prob factor, if necessary
    # WARNING! Only for proportionality and flux shape.
    # This will mess up with absolute normalization!
    if applyDecayProb:
        decayProb = K.DecayProbability(df['bins'],nMass)
    else:
        decayProb = 1
    
    # Enhancement factors
    k_e_factor = K.kFactor('K','e',nMass)
    k_mu_factor = K.kFactor('K','mu',nMass)
    pi_e_factor = K.kFactor('pi','e',nMass)
    pi_mu_factor = K.kFactor('pi','mu',nMass)
    k0_e_factor = K.k0Factor('e',nMass)
    k0_mu_factor = K.k0Factor('mu',nMass)
    mu_factor = K.muonFactor(nMass)
    incpi_factor = K.incpiFactor('e',nMass)
    other_factor = K.otherFactor(nMass)
    
    # \mu component
    df['numu_pi'] = data['flux']['numu_pi'] * pi_mu_factor * theta_mu2 * decayProb
    df['numu_k'] = data['flux']['numu_k'] * k_mu_factor * theta_mu2 * decayProb
    df['numu_pifromk+'] = data['flux']['numu_pifromk+'] * pi_mu_factor * theta_mu2 * decayProb
    df['numu_pifromk0'] = data['flux']['numu_pifromk0'] * pi_mu_factor * theta_mu2 * decayProb
    df['numu_others'] = data['flux']['numu_others'] * other_factor * theta_mu2 * decayProb
    df['anumu_pi'] = data['flux']['anumu_pi'] * pi_mu_factor * theta_mu2 * decayProb
    df['anumu_mufrompi'] = data['flux']['anumu_mufrompi'] * mu_factor * theta_mu2 * decayProb
    df['anumu_others'] = data['flux']['anumu_others'] * other_factor * theta_mu2 * decayProb
    # e component
    df['nue_mufrompi'] = data['flux']['nue_mufrompi'] * mu_factor * theta_e2 * decayProb
    df['nue_k'] = data['flux']['nue_k'] * k_e_factor * theta_e2 * decayProb
    df['nue_k_incpi'] = data['flux']['nue_k_incpi'] * incpi_factor * theta_e2 * decayProb
    df['anue_k0'] = data['flux']['anue_k0'] * k0_e_factor * theta_e2 * decayProb
    df['anue_mufrompi'] = data['flux']['anue_mufrompi'] * mu_factor * theta_e2 * decayProb
    
    # Remove unphysical steriles with negative rest energy
    for i,bins in enumerate(df['bins'][df['bins']<nMass]):
        for channel in df:
            if channel!='bins':
                df[channel][i] = 0.
    
    # Calculate total flux
    df['total'] = df['numu_pi'] + df['numu_k'] + df['numu_others'] + df['anumu_pi'] + df['anumu_mufrompi'] + df['anumu_others'] + df['nue_mufrompi'] + df['nue_k'] + df['anue_k0'] + df['anue_mufrompi']

    # Convert 'nan' values to zeroes
    df['total'] = np.nan_to_num(df['total'])

    return df