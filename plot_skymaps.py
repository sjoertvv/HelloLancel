'''
run this after make_skymaps and run_MC to make plot
'''

from setup_ice import iceberg
from load_data import data, data_ac
from make_skymaps import *

import sjoert



def sky_fin():
	# plot the plane in RA Dec
	for lb in [-1*min_b, min_b]:
		bb = np.repeat(lb, 2000)
		ll = np.linspace(0.1,359, len(bb))
		rr, dd =sjoert.stellar.lbtoradec(ll, bb)
		plt.plot(rr, dd, '.', ms=1, color='grey', zorder=1)

	cc = iceberg['area']
	#plt.scatter(iceberg['RA'], iceberg['Dec'], s=cc,marker='o', edgecolor='k', facecolor='cyan')	

	for ic in iceberg:
		#circle1 = plt.Circle((ic['RA'], ic['Dec']), np.sqrt(ic['area']/np.pi), color='cyan')
		#plt.gca().add_patch(circle1)

		rectangl1= plt.Rectangle( (ic['RA']-ic['RA_min'],ic['Dec']-ic['Dec_min']), 
			ic['RA_min']+ic['RA_plus'],
			ic['Dec_min']+ic['Dec_plus'], 
			facecolor='cyan',
			lw=0.5,
			edgecolor='k')  

		plt.gca().add_patch(rectangl1)

	plt.ylim(-30, 90)
	plt.xlim(0, 360)
	plt.xlabel('Right Ascension (deg)')
	plt.ylabel('Declination (deg)')


plt.close()
plt.figure(1,(8,4))
plt.plot(data_ac['ra'], data_ac['dec'], 'xk', alpha=0.9)
plt.scatter(data_ac['ra'], data_ac['dec'], color='k', marker='s', alpha=0.9,s=0.1, zorder=1)

sky_fin()
cbar = plt.colorbar()
cbar.remove()
plt.title('IceCube neutrino alerts and {0} accretion flares'.format(len(data_ac)))
plt.pause(0.1)
key = input('next?')


# plot the 2D histogram
plt.clf()
h =plt.hist2d(data['ra'], data['dec'], bins=40, cmap='cubehelix_r')
sky_fin()
cbar = plt.colorbar()
cbar.set_label('Number per bin', size=12)
plt.title('IceCube neutrino alerts and ZTF nuclear transient density')
plt.pause(0.2)
key = input('next?')


plt.clf()
nbins=150
h, x, y, p = plt.hist2d(ps_Sky['ra'], ps_Sky['dec'], bins=nbins, cmap='cubehelix_r')
plt.clf()
plt.pcolormesh(np.linspace(0,360, nbins), np.linspace(min(ps_Sky['dec']), max(ps_Sky['dec']), nbins), h.T/1e4, 
	shading='gouraud',snap=True, cmap='cubehelix_r')

sky_fin()
cbar = plt.colorbar()
cbar.set_label(r'Number per bin ($\times 10^4$)', size=12)
plt.title('IceCube neutrino alerts and density of background samples')
plt.pause(0.2)
key = input('next?')


plt.clf()
nbins=100
h, x, y, p = plt.hist2d(twomxz_ra,twomxz_dec, bins=nbins, cmap='cubehelix_r')
plt.clf()
plt.pcolormesh(np.linspace(0,360, nbins), np.linspace(min(ps_Sky['dec']), max(ps_Sky['dec']), nbins), np.clip(h.T/1e4, 0,0.002), 
	shading='gouraud',snap=True, cmap='cubehelix_r')
sky_fin()
cbar = plt.colorbar()
cbar.set_label(r'Number per bin ($\times 10^4$)', size=12)
plt.title('IceCube neutrino alerts and density of 2MASS galaxies')
plt.pause(0.2)
key = input('next?')


plt.clf()
values = np.vstack([data['ra'], data['dec']])
kernel_test = scipy.stats.gaussian_kde(values, bw_method=0.2) #'silverman'


xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = kernel_control(np.vstack([xi.flatten(), yi.flatten()]))

plt.pcolormesh(xi, yi, zi.reshape(xi.shape)*1e5, shading='gouraud',snap=False, cmap='cubehelix_r')

sky_fin()
plt.title('IceCube alerts and KDE of ZTF nuclear transients')
cbar = plt.colorbar()
cbar.set_label(r'Probability density ($\times 10^{-5}$)', size=12)
plt.pause(0.2)
key = input('next?')
