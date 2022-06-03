import numpy as np
import astropy.io.fits
import os
import scipy

import k3match

from sjoert.stellar import radectolb

from hellolancel.load_data import data, data_dir, settings
from hellolancel.setup_ice import iceberg


# also try to make a collection of non-AGN flares
twomassXz = astropy.io.fits.getdata(os.path.join(data_dir, '2MASS/XSCz_Huchra_velmod.fit'))

Nsky = int(1e6)  # number of events sampled from ZTF sky dist

min_b = settings['min_b'] # define the Galactic plane


# cuts for 2MASS
itx = twomassXz['dec']>min(data['dec'])
itx *= twomassXz['dec']<max(data['dec'])
twomxz_ra,twomxz_dec  = twomassXz[itx]['ra'], twomassXz[itx]['dec']
print ('# of 2MASSXz sources:\t', len(twomxz_ra))


# ----
# define control sample (everything)
icontrol = np.repeat(True, len(data))
print ('# of flares in control sample:', sum(icontrol))


n_control = sum(icontrol)

print ('creating array for sky sampling....')

ps_Sky = np.zeros(Nsky, dtype=[('ra', 'f8'),('dec', 'f8')])

print ('KDE fitting...')

values = np.vstack([data[icontrol]['ra'], data[icontrol]['dec']])
kernel_control = scipy.stats.gaussian_kde(values, bw_method='scott') # was 0.15
#kernel_control = scipy.stats.gaussian_kde(values)
kde_out = kernel_control(values)
kde_max = np.max(kde_out)

print ('building interpolation grid for kernel...')

ra_arr = np.linspace(0,360, 360*2)
dec_arr = np.linspace(-30, 87, (87+30)*2 )
kde_grid = np.zeros((len(ra_arr), len(dec_arr)))

# for-loop to keep it easy
for i, ra in enumerate(ra_arr):	
	l,b = radectolb(ra, dec_arr)
	joutplane = np.abs(b)>min_b
	kde_grid[i,joutplane]=kernel_control(np.vstack([np.repeat(ra, sum(joutplane)), dec_arr[joutplane]]))

print ('building interpolation function for kernel...')

kernel_inter = scipy.interpolate.RegularGridInterpolator((ra_arr, dec_arr), kde_grid, method='linear')
print ('sampling ZTF coodindates...')

zt1 = np.linspace(0,1, n_control)
ra_sort = np.sort(data[icontrol]['ra'])
dec_sort = np.sort(data[icontrol]['dec'])

ps_Sky['ra']  = np.random.rand(len(ps_Sky))*360
ps_Sky['dec'] = np.random.rand(len(ps_Sky))*(max(dec_arr)-min(dec_arr))+min(dec_arr)

these_kern = kernel_inter(np.array([ps_Sky['ra'], ps_Sky['dec']]).T)
uni_sample = np.random.rand(len(ps_Sky))*kde_max

idx_keep = np.where(  (these_kern>uni_sample) )[0]
idx_rejsam = np.where(  (these_kern<uni_sample) )[0]

print ('# rejecting based on kde  :', len(idx_rejsam))

while 1:

	ps_Sky['ra'][idx_rejsam]  = np.random.rand(len(idx_rejsam))*360
	ps_Sky['dec'][idx_rejsam] = np.random.rand(len(idx_rejsam))*(max(dec_arr)-min(dec_arr))+min(dec_arr)
	
	these_kern = kernel_inter(np.array([ps_Sky['ra'][idx_rejsam], ps_Sky['dec'][idx_rejsam]]).T)
	uni_sample = np.random.rand(len(idx_rejsam))*kde_max
	
	idx_rejsam = idx_rejsam[np.where( (these_kern<uni_sample) )[0]]
	print ('# rejecting based on kde  :', len(idx_rejsam))
	if len(idx_rejsam)==0:
		break


print ('computing fraction in footprint...')
for i, ice in enumerate(iceberg):

	rra = np.arange(ice['RA']-ice['RA_min'], ice['RA']+ice['RA_plus'], 0.2)
	ddec = np.linspace(ice['Dec']-ice['Dec_min'], ice['Dec']+ice['Dec_plus'], len(rra))
	t1, t2, t12 = k3match.celestial(rra, ddec, ps_Sky['ra'], ps_Sky['dec'], 0.25)
	l,b = radectolb(ice['RA'], ice['Dec'])
	iceberg['finfoot'][i] = len(np.unique(t1)) / len(rra)
	print (ice['Event'], 'b={0:5.1f}, fraction in footprint : {1:0.3f}'.format(b, iceberg['finfoot'][i]))





