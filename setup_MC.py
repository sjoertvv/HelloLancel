'''
make samples of accretion flares for H0
'''

from matplotlib import pyplot as plt
import numpy as np
import pickle
import random

from TS_input import get_icoin, flux_check_key 

import k3match

# local imports
from setup_ice import iceberg
from load_data import data, data_ac, settings
from make_skymaps import ps_Sky, icontrol, twomxz_ra,twomxz_dec


# settings
do_twomass = settings['do_twomass'] 	# use KDE of ZTF nuclear transient (or 2MASS if False)
Ntest = settings['Ntest']				# number of MC samples used


# dtype for the Monte Carlo sample of flares
min_z_dtype = [('ran_id', 'i8'),('ra', 'f8'),('dec', 'f8'),
			('flare_peak_jd', 'f8'), ('echo_duration_w1', 'f8'),
			(flux_check_key, 'f8'),
			('pre_rms_flux_w1', 'f8'), ('df_over_rms', 'f8'), ('flare_postpeak_duration_day', 'f8')]


n_pst = len(data_ac)
ps_test_copy = np.zeros(n_pst, dtype=min_z_dtype)

for k in ps_test_copy.dtype.names[3:]:
 	ps_test_copy[k] = data_ac[k].copy()


print ('creating empty MC flare sample....')
ps_Ntest = np.tile(ps_test_copy, Ntest)
ps_Ntest['ran_id'] = np.repeat(np.arange(Ntest), n_pst)

print ('assigning random RA/Dec to MC sample...')

print ('making unique random indices...')
iran_control = np.zeros(len(ps_Ntest), int)
iran_flares = np.zeros(len(ps_Ntest), int)
iran_off = np.zeros(len(ps_Ntest), int)
n_control = sum(icontrol)

for i in range(Ntest):
	iran_control[i*n_pst:(i+1)*n_pst] =  random.sample(range(0, n_control), n_pst)
	iran_flares[i*n_pst:(i+1)*n_pst] =  random.sample(range(0, n_pst), n_pst)

# from KDE
if not do_twomass:

	iran = np.array(np.random.rand(len(ps_Ntest)) * len(ps_Sky), int) 
	ps_Ntest['ra']  = ps_Sky['ra'][iran]
	ps_Ntest['dec'] = ps_Sky['dec'][iran]

# or 2MASS
else:
	
	# use 2MASSx
	iran_2m = np.random.randint(0, len(twomxz_ra), size=len(ps_Ntest))
	ps_Ntest['ra'] = twomxz_ra[iran_2m]
	ps_Ntest['dec'] = twomxz_dec[iran_2m]


# also reorder the time of peak 
ps_Ntest['flare_peak_jd'] = data_ac['flare_peak_jd'][iran_flares]


# now we can match 
max_match_rad = 10  # this should be >10, such that it has no effect on the outcome, just speeding up the calculation
print ('\nmatching....')
t1, t2, t12 = k3match.celestial(iceberg['RA'], iceberg['Dec'], ps_Ntest['ra'],ps_Ntest['dec'], max_match_rad)


# to speed things up, remove matches that are certainty outside 90% radius 
print ('quick trimming based on max radius...')
imaxr = t12<1.1*iceberg[t1]['max_rad']
t1 = t1[imaxr]
t2 = t2[imaxr]
t12 = t12[imaxr]

print ('applying indices...')
ice_match = iceberg[t1]

print ('coincidence check...')
icoin = get_icoin(ice_match, ps_Ntest[t2])


print ('making final array with coincident matches...')
iceberg_Ntest_coin = ice_match[icoin]
iceberg_Ntest_coin['ran_id'] = ps_Ntest['ran_id'][t2][icoin]

uni_ice_events = np.unique(iceberg_Ntest_coin['Event'])
iceberg_coin = iceberg[[np.where(iceberg['Event']==evnt)[0][0] for evnt in uni_ice_events]]

print ('# of unique IceCube events coincident in random sample:', len(uni_ice_events))
print ('# of unique flares that match, ',  len(np.unique(ps_Ntest[flux_check_key][t2][icoin])))

ps_matched_names = []
for flux in np.unique(ps_Ntest[flux_check_key][t2][icoin]):
	ps_matched_names.append(data_ac[data_ac[flux_check_key]==flux]['name'][0])


print ('accretion flares missing in MC sample:')
ps_missing_names = np.setdiff1d(data_ac['name'],ps_matched_names )
for nm in ps_missing_names:
	ps = data_ac[data_ac['name']==nm][0]
	print (ps['name'], ps['flare_postpeak_duration_day'])

# store the flare properties into the coincident matches
iceberg_Ntest_coin['flux_weight'] = ps_Ntest[flux_check_key][t2][icoin]
iceberg_Ntest_coin['log10_df_over_rms'] = np.log10(ps_Ntest['df_over_rms'][t2][icoin])


# compute the ncoin parameter: the number of background flares matched to this neutrino
# this includes neutrinos matched to multiple ZTF sources in one MC realization
print ('computing ncoin...')
finfoot = np.zeros(len(uni_ice_events))
for i, evnt in enumerate(uni_ice_events):
	idx = np.where(iceberg_Ntest_coin['Event']==evnt)[0]
	#ncoin_tde = sum(p_one_min_ratio(iceberg_Ntest_coin['log10_df_over_rms'][idx]))/Ntest # original for 1st submission (not used in output)
	ncoin_tde = len(idx)/Ntest
	iceberg['ncoin'][iceberg['Event']==evnt]= ncoin_tde 
	iceberg_Ntest_coin['ncoin'][idx] = ncoin_tde

mean_signalness = 0
for evnt in uni_ice_events:
	mean_signalness+=sum(iceberg_Ntest_coin[iceberg_Ntest_coin['Event']==evnt]['signalness'])
mean_signalness/=len(iceberg_Ntest_coin)

# use the power of numpy to avoid a large forloop
idx_sort = np.argsort(iceberg_Ntest_coin['ran_id'])
iceberg_Ntest_coin_sort = iceberg_Ntest_coin[idx_sort]
events_coin_sort = iceberg_Ntest_coin_sort['Event']

vals, idx_start, count = np.unique(iceberg_Ntest_coin_sort['ran_id'], return_counts=True, return_index=True)
idx_Ntest = np.split(idx_sort, idx_start[1:])


# count unique neutrino-echo pairs
nrandom_matches = np.array([len(np.unique(events_coin_sort[ii])) for ii in idx_Ntest])
id_nomatch = np.setdiff1d(np.arange(Ntest), vals)

mean_ncoin_cut = np.mean(np.append(nrandom_matches, np.zeros(len(id_nomatch))))

n_check = len(iceberg_Ntest_coin)/Ntest

total_ice_area = sum( np.unique(iceberg_Ntest_coin['area']*iceberg_Ntest_coin['finfoot']) )

ftcoin_all = np.zeros(len(iceberg_coin))
for i, ic in enumerate(iceberg_coin):
	tdiff =  ic['jd'] - data[icontrol]['flare_peak_jd']
	ftcoin_all[i] += 365-np.clip(min(tdiff), 0, 1e99)

print ('sum signalness                         :',sum(iceberg_coin[ftcoin_all>0]['signalness']))
print ('total IC area in footprint             : {0:0.1f}'.format(total_ice_area))
print ('background source count expectation    : {0:0.4f}'.format(sum(iceberg['ncoin'])))
print ('background source density              : {0:0.3e}'.format(sum(iceberg['ncoin'])/total_ice_area))

