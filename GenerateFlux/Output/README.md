Flux files generated with Owen's new flux generator.
Please note, code is hardcoded for mu-pi decays only, with theta_e2 = 0 and nominal theta_mu2 = 1 (need to downscale for realistic mixing angle values).

0_OldFluxFiles_ScalingMethod:
- Contains files previously used for the analysis. Just scaling the BNB nu flux by the mixing angle and apply correction kinematic factor.

1_Flux_TraversingMicroBooNE_UNSCALED:
- Fluxes of HNL TRAVERSING THE DETECTOR with NOMINAL mixing angle of 1 (they are not scaled by mixing angle yet) determined with Owen simulation method.
Units are x: GeV and y: Flux/POT/cm^2/GeV

2_Flux_DecayingInMicroBooNE:
Fluxes of HNL which have been scaled down to a mixing angle and to which have been applied the decay probability for mupi decay (with correct normalisation).
These files effectively represent the HNL DECAYING inside the detector (e.g. integrating gives the total number of decays and flux can be used for MC generation).
Units are x: GeV and y: Flux/POT/cm^2/GeV
