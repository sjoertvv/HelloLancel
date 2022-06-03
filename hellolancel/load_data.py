'''
load the flare data and define the input settings of the likelihood analysis
'''

import astropy.io.ascii
from hellolancel.settings import settings
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")

fname = os.path.join(data_dir, 'ZTF_NEOWISE/ZTF_neoWISE_flares_parent.dat')

# read the parent sample of all nuclear transient with post-peak neoWISE observations
data = astropy.io.ascii.read(fname)

# the sample of accretion flares with potential dust echoes
data_ac = astropy.io.ascii.read(fname.replace('_parent','_acflares'))

# the sample of accretion flares with potential dust echoes
data_allztf = astropy.io.ascii.read(fname.replace('_parent','_allztf'))

if settings['do_all_ZTF']:
	data_ac = data_allztf