'''
estimate the significance of 3 neutrino detections from large dust echoes 
here we use only their low sky density, no Monte Carlo is used here
'''
import scipy.stats
import numpy as np

from sjoert.stellar import radectolb

from hellolancel.load_data import data_ac
from hellolancel.setup_ice import iceberg
from hellolancel.TS_input import get_icoin, pval_to_sigma

# estimate fraction of time a neutrino is in temportal coincidence with a flare
ntcoin = np.zeros(len(iceberg))
for i, ic in enumerate(iceberg):
	for dd in data_ac:
		ntcoin[i] += get_icoin(ic, dd, only_tdiff=True)
duration_correction = sum(ntcoin)/ (len(ntcoin)*len(data_ac))
print ('probability a neutrino arrives the window for a temporal match to a flare: {0:0.3f}'.format(duration_correction))

# keep IceCube alerts inside the ZTF footprint
l, b= radectolb(iceberg['RA'], iceberg['Dec']) 
ioutplane = np.abs(b)>8

# get the total area of all IC alerts in the footprint
total_ice_area = np.sum(iceberg[ioutplane]['area'])
print ('sum of neutrino 90%CL reconstruction area for events within the footprint: {0:0.1f} deg'.format(total_ice_area))

# if we account for the fraction of the 90%CL are that falls inside the plane, we get a slighty lower value (and the significance changes by 0.02 sigma)
total_ice_area = 698.6

# select large echoes to yield only real TDE-like events
# we pick a round number (for the likelihood analysis no cuts are needed)
large_echo_cut = 10

#large_echo_cut = 15 # FYI - this is the echo strength of Lancel (the third event), cutting here would be similar to doing a p-value scan  

# extra-galactic sky seen by ZTF in deg^2 taken from Stein et al. (2021)
sky_ztf =  28000 		

# effective number of flares
N_eff = sum(data_ac['df_over_rms']>large_echo_cut) * duration_correction 

# effective desnity of flares
n_eff = N_eff/sky_ztf 

# expected number of backround matches
n_expect = n_eff * total_ice_area

n_observed = 3 # the observed flares with a neutrino counterpart

p_prob = 1-scipy.stats.poisson.cdf(n_observed-1,n_expect)
print ('Poisson probability to observe >=3 when {0:0.2f} are expected: {1:0.1e}'.format(n_expect, p_prob))
print ('this is {0:0.2f} sigma'.format(pval_to_sigma(p_prob)))






