import math
import numpy as np
import sys, os

import Functions.EventRates as ER


POT = 6e20 # protons on target, three years livetime [uBooNE proposal]
mass = 0.350 # GeV
theta_e2 = 1e-7
theta_mu2 = 1e-7

microBooneEvents_mupi = ER.EventRate_MuPi(mass,theta_e2,theta_mu2,POT)
# microBooneEvents_epi = ER.EventRate_Nu2EPi(mass,theta_e2,theta_mu2,POT)

print microBooneEvents_mupi
