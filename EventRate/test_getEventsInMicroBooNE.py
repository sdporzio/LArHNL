import math
import numpy as np
import sys, os
import Functions.EventRates as ER

### SETTINGS
mass = 0.350 # GeV
theta_mu2 = 1e-7
POT = 2e20 # protons on target, three years livetime [uBooNE proposal]
detector = 'microboone'

### RUN FUNCTION
microBooneEvents_mupi, _, _ = ER.EventRate_MuPi(mass,theta_mu2,POT,detector)
print("Number of events in %s fiducial volume\nfor HNL with mass %.3f GeV, %.0e mixing angle\nand with a %.1e POT exposure:\n" %(detector, mass, theta_mu2, POT))
print("%.1f events" %microBooneEvents_mupi)
