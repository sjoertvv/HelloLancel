'''
this script combines everything to obtain the 
TS distribution for the data and MCed background
'''

from sjoert.stellar import ang_sep
import matplotlib.pyplot as plt

import importlib
from hellolancel import TS_input
importlib.reload(TS_input)

from hellolancel.TS_input import test_stat_only_coin, pval_to_sigma
from hellolancel.setup_MC import *
from hellolancel.setup_ice import iceberg
from hellolancel.load_data import data_ac

# mean source density
bg_areal_dens = sum(iceberg['ncoin'])/total_ice_area			

# find coincident matches for data
iceberg_coin_obs = np.zeros(0,dtype=iceberg.dtype)

for ic in iceberg: 
	icoin= get_icoin(ic, data_ac)
	ic_coin = np.repeat(ic.copy(), sum(icoin)) # allow multiple matches (fixed below)
	ic_coin['flux_weight'] = data_ac[icoin][flux_check_key]
	ic_coin['log10_df_over_rms'] = np.log10(data_ac[icoin]['df_over_rms'])
	ic_coin['mdist'] = ang_sep(ic['RA'],ic['Dec'], data_ac[icoin]['ra'], data_ac[icoin]['dec'])
	iceberg_coin_obs = np.append(iceberg_coin_obs, ic_coin)
	if sum(icoin):
		print ('IC alert:', ic['Event'])
		for i, tic in enumerate(ic_coin):
			print ('ZTF name: {0}; match dist: {1:0.1f} deg'.format(data_ac[icoin]['name'][i], tic['mdist']))
			

# ---
# here starts the likelihood ratio estimate

def test_stat(ice_in, return_SB=False):
	return test_stat_only_coin(
			ice_in,  
			bg_areal_density = bg_areal_dens, 
			return_SB = return_SB)

ts_obs_arr = test_stat(iceberg_coin_obs)

# make new array for the observed neutrinos that are coindicent with observed sample
ts_obs_arr = test_stat(iceberg_coin_obs)
SB_spatial,SB_flux,SB_df = test_stat(iceberg_coin_obs, return_SB=True)


ts_obs = 0. 
Nice_obs = 0
for evnt in np.unique(iceberg_coin_obs['Event']):
	ie = iceberg_coin_obs['Event']==evnt
	ts_obs+=np.max(ts_obs_arr[ie])
	Nice_obs+=1

print ('# of coincident events:', Nice_obs)
print ('TS for observations   : {0:0.3f}'.format(ts_obs))

# now run on the MCed backround samples
print ('applying TS to MCed samples...')
ts_arr = np.zeros(Ntest)
test_stat_sort = test_stat(iceberg_Ntest_coin_sort)

ts_arr_single = np.zeros(Ntest)

print ('checking for multiple matches to one neutrino...')
for l in range(len(vals)):
	
	# do booking keeping for multiple echoes matched to one neutrino
	these_events = events_coin_sort[idx_Ntest[l]]
	l_idx_sort = np.argsort(these_events)
	these_events = these_events[l_idx_sort]	
	these_ts = test_stat_sort[idx_Ntest[l]][l_idx_sort]
	l_vals, l_idx_start, l_count = np.unique(these_events, return_counts=True, return_index=True)
	these_ts_slit = np.split(these_ts, l_idx_start[1:])
		
	these_ts_slit_maxl = [np.max(x) for x in these_ts_slit]

	ts_arr[vals[l]] = np.sum(these_ts_slit_maxl)
	ts_arr_single[vals[l]] = these_ts_slit_maxl[0]


nlarger = sum(ts_arr>=ts_obs)
pval = nlarger /Ntest

print ('# MCed samples that are larger, ', nlarger)
print ('p-value: {0:0.3e} (={1:0.3f} sigma)'.format(pval, pval_to_sigma(pval)))


nlarger_woL = sum(ts_arr>=sum(ts_obs_arr[iceberg_coin_obs['Event']!='IC191119A']))
pval_woL = nlarger_woL /Ntest
print ('\n[w/o AT2019aalc: p-value: {0:0.3e} (={1:0.3f} sigma)]'.format(pval_woL, pval_to_sigma(pval_woL)))


plt.clf()
plt.hist(ts_arr,bins=51, density=True, color='darkgrey', label='Background')
base  =  np.floor(np.log10(pval))
plt.axvline(ts_obs,color='midnightblue',  label=r'Observations, $p={0:0.1f}\times 10^{{{1:0.0f}}}$'.format(pval/10**base, base))
plt.xlabel('Test statistic')
plt.legend()
plt.ylabel('Probability density')
plt.yscale('log')
plt.ylim(7e-7, 0)
plt.xlim(-0.5, ts_obs+6)
plt.pause(0.1)
key = input('done.')










