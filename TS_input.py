'''
compute the signal and background PDFs of echo strength and flux

also here we define the function for coincidence and the TS
'''

import numpy as np
from pylab import plt
import scipy.stats

from load_data import data, data_ac, data_allztf, settings

# conf function
def pval_to_sigma(pval):
	ff = np.linspace(1,5,1000)
	return np.interp(pval, 1-(scipy.stats.norm.cdf(ff,0,1))[::-1], ff[::-1])


# define time window for IceCube+ZTF matches
tdiff_max = settings['tdiff_max']
tdiff_min = settings['tdiff_min']

# defaults
flux_check_key = 'post1yr_mean_flux_w1' # define the echo flux
bw = 'scott'  		# bandwidth for KDE; 'scott' method: N**(-1./(1+4))
cc_dict = {'TDE':'midnightblue', 
			'not TDE':'seagreen', 
			'AGN':'darkgrey', 
			'AC flare':'pink', 
			'Parent sample':'seagreen'}


# define the indices to classes
itde = (data['qclass']=='TDE?')  + (data['qclass']=='TDE') 
iac = np.array([x in data_ac['name'] for x in data['name']])
inottde = (itde==False) 
iagn = (data['qclass']=='AGN') 
isn = data['qclass']=='SN' 
iw1detect = (data[flux_check_key]>0)
iparent = iw1detect 

kernel_strength = {}
kernel_flux = {}

for k, ii in zip(('AC flare', 'not TDE', 'TDE', 'AGN', 'Parent sample'),\
 	(iac, inottde*iac, itde*iac, iagn*iac, iparent)):

	strength_use = np.array(np.log10(data[ii]['df_over_rms']))
	flux_use = np.log10(np.array(data[ii][flux_check_key]))

	if len(strength_use)>1:
		
		kernel_strength[k] = scipy.stats.gaussian_kde(strength_use, bw_method=bw)
		kernel_flux[k] = scipy.stats.gaussian_kde(flux_use, bw_method=bw)


# the PDFs for each source class
def p_flux(log10_flux, cl):
	'''
	helper function to get the KDE for the echo flux of each class
	'''
	return kernel_flux[cl](log10_flux)

def p_strength(log10_strength, cl):
	'''
	helper function to get the KDE for the echo strength of each class
	'''
	return kernel_strength[cl](log10_strength)

norm_lin = max(data_ac[flux_check_key])-min(data_ac[flux_check_key])
xx_lin = np.linspace(min(data_ac[flux_check_key]),max(data_ac[flux_check_key]), 10000)
norm_log = np.trapz(xx_lin,np.log10(xx_lin))

def p_flux_linear(log10_strength, norm=norm_log):
	'''
	linear PDF for echo flux:
	P ~ flux
	'''	
	return 10**log10_strength / norm_log

# define the signal and background PDFs
def p_flux_bg(log10_flux):
	return p_flux(log10_flux, 'Parent sample')

def p_flux_sig(log10_flux):
	return p_flux_linear(log10_flux)

def p_strength_bg(log10_strength):
	return p_strength(log10_strength, 'not TDE')

def p_strength_sig(log10_strength):
	return p_strength(log10_strength, 'TDE')



def get_icoin(ice_in, photo_in,
		tdiff_max=tdiff_max, 
		tdiff_min=tdiff_min, 
		do_all_ZTF=settings['do_all_ZTF'],
		return_tdiff=False, only_tdiff=False, verbose=False):
	'''
	apply the temporal and spatial coincidence check
	input IceCube and flare data need to have same length (ie, already matched with some large radius) 
	return booling array with coincidences	
	'''
	if verbose:
		print ('extracting RA/Dec/JD from')
	ztf_ra, ztf_dec, ztf_jd, ztf_duration, echo_duration = \
		photo_in['ra'], photo_in['dec'], photo_in['flare_peak_jd'], photo_in['flare_postpeak_duration_day'], photo_in['echo_duration_w1']


	if verbose:
		print ('tdiff...')
	tdiff = ice_in['jd'] - ztf_jd
	itdiff = (tdiff < tdiff_max) * (tdiff > tdiff_min) 

	# require neoWISE difference flux detection when/after neutrino arrives
	itdiff *= (tdiff<echo_duration)
	
	# require post-peak ZTF detection when/after neutrino arrives
	if not do_all_ZTF:
		itdiff *= (tdiff<ztf_duration) 
	
	if only_tdiff:
		if return_tdiff:
			return itdiff, tdiff

		return itdiff

	
	ira_min = ztf_ra > (ice_in['RA']-ice_in['RA_min'])
	if verbose:
		print ('RA max...')
	ira_max = ztf_ra < (ice_in['RA']+ice_in['RA_plus'])
	if verbose:
		print ('Dec min...')
	idec_min = ztf_dec > (ice_in['Dec']-ice_in['Dec_min'])
	if verbose:
		print ('Dec max...')
	idec_max = ztf_dec < (ice_in['Dec']+ice_in['Dec_plus'])


	# collect the results into a final array with the coindicent events
	if verbose:
		print ('combining...')
	
	icoin = (ira_min*ira_max*idec_min*idec_max) * itdiff
	
	if return_tdiff:
		return icoin, tdiff
	
	return icoin



def test_stat_only_coin(ice_in, 
				flux_norm = None,
				bg_areal_density = None,
				mean_signalness = None,
				return_SB=False):
	'''
	compute the test statistic for a single flare-neutrino coincident match
	input with a catalog with the flare and neutrino properties
	'''
	
	if bg_areal_density is None:
		bg_areal_density =ice_in['ncoin']/ice_in['area']	# bg source density for this neutrino
	
	# signalness weight term
	SB_IC = ice_in['signalness'] 

	# expection 
	nsig = 0.9 / ice_in['area']
	nbg = bg_areal_density 			
 
	SB_spatial = nsig / nbg  

	x_in = np.log10(ice_in['flux_weight'])
	SB_flux = p_flux_sig(x_in) / p_flux_bg(x_in) 
	
	x_in = ice_in['log10_df_over_rms']
	SB_df = p_strength_sig(x_in)/p_strength_bg(x_in)
	
	if return_SB:
		return 2*np.log(SB_spatial), 2*np.log(SB_flux), 2*np.log(SB_df)

	return 2*np.log(np.clip(SB_IC * SB_spatial * SB_flux * SB_df, 1,1e99)) #



