'''
load the flare data and define the input settings of the likelihood analysis
'''

import astropy.io.ascii 

fname = 'data/ZTF_NEOWISE/ZTF_neoWISE_flares_parent.dat'

# read the parent sample of all nuclear transient with post-peak neoWISE observations
data = astropy.io.ascii.read(fname)

# the sample of accretion flares with potential dust echoes
data_ac = astropy.io.ascii.read(fname.replace('_parent','_acflares'))

# the sample of accretion flares with potential dust echoes
data_allztf = astropy.io.ascii.read(fname.replace('_parent','_allztf'))


#--------
# also define global settings for the likelihood anaylsis
settings = {}

settings['do_twomass'] 	= False 	# default is to use the KDE of the RA, Decl. of the parent sample
settings['do_all_ZTF'] 	= False   	# if True, we make no selection on the optical properties of the flare, simply select all dust echo candidates
settings['Ntest']		= int(1e6) 	# number of Monte Carlo samples 1e5 is fast but not enough, 1e6 is used for publication (if do_twomass==True, 1e6 is overkill, and you can use 1e5)
settings['min_b'] 		= 8 		# Galatic lattitude to define the plane (inside the plane we force zero flares for the MC samples)

if settings['do_all_ZTF']:
	data_ac = data_allztf