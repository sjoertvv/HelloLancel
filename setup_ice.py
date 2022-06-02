'''
compile IceCube alert info
'''

from matplotlib import pyplot as plt
import astropy.io.ascii
import numpy as np
import k3match
import sjoert

ice_GB0 =  astropy.io.ascii.read('./data/IC/AMON_ICECUBE_GOLD_AND_BRONZE.dat')
ice_EHE0 =  astropy.io.ascii.read('./data/IC/AMON_ICECUBE_EHE.dat')
ice_HESE0 =  astropy.io.ascii.read('./data/IC/AMON_ICECUBE_HESE.dat')
iceberg0 =  astropy.io.ascii.read('./data/IC/IC_alerts_merged.txt')


# add new fields
print ('total number of icecube events:',len(iceberg0))
iceberg0['signalness'] = np.zeros(len(iceberg0))
iceberg0['area'] = np.zeros(len(iceberg0))
iceberg0['jd'] = np.zeros(len(iceberg0))
iceberg0['max_rad'] = np.zeros(len(iceberg0))
iceberg0['R50'] = np.zeros(len(iceberg0))
iceberg0['ran_id'] = np.zeros(len(iceberg0), int)
iceberg0['mdist'] = np.zeros(len(iceberg0))
iceberg0['ncoin'] = np.zeros(len(iceberg0))
iceberg0['flux_weight'] = np.zeros(len(iceberg0))
iceberg0['log10_df_over_rms'] = np.zeros(len(iceberg0))
iceberg0['finfoot'] = np.zeros(len(iceberg0))

iceberg0 = np.array(iceberg0) # freeze


for i, ice in enumerate(iceberg0):

	area_sq = (ice['RA_min']+ice['RA_plus'])*(ice['Dec_min']+ice['Dec_plus']) # crude estimate

	# compute the area for the rectangular region
	theta_min =  (90-ice['Dec']-ice['Dec_min'])/180*np.pi
	theta_plus = (90-ice['Dec']+ice['Dec_plus'])/180*np.pi
	phi_min = (ice['RA']-ice['RA_min'])/180*np.pi
	phi_plus = (ice['RA']+ice['RA_plus'])/180*np.pi
	area_rad = (np.cos(theta_min)-np.cos(theta_plus))*(phi_plus-phi_min)
	area_deg = area_rad/(4*np.pi) *41252.96
	
	#print (ice['Dec'], area_sq, area_deg)
	iceberg0[i]['area'] = area_deg

	date_str = '20{0}-{1}-{2}'.format(ice['Event'][2:4], ice['Event'][4:6], ice['Event'][6:8])
	iceberg0[i]['jd'] = astropy.time.Time(date_str).jd
	q1 = np.sqrt(ice['RA_min']**2+ice['Dec_min']**2)
	q2 = np.sqrt(ice['RA_min']**2+ice['Dec_plus']**2)
	q3 = np.sqrt(ice['RA_plus']**2+ice['Dec_plus']**2)
	q4 = np.sqrt(ice['RA_plus']**2+ice['Dec_min']**2)

	iceberg0[i]['max_rad'] = max(max(max(q1,q2), max(q2,q3)),ice['R50'])


for i in range(len(iceberg0)):
	event_str =  iceberg0[i]['Event']
	date_str = '{0}/{1}/{2}'.format(event_str[2:4], event_str[4:6], event_str[6:8])
	idx = np.where(ice_GB0['Date']==date_str)[0]
	if len(idx):
		#print (i, event_str,ice_GB0[idx[0]]['Rev'], ice_GB0[idx[0]]['Error90_arcmin']/60)
		iceberg0[i]['signalness'] = ice_GB0[idx[0]]['Signalness']
		iceberg0[i]['R50'] = ice_GB0[idx[0]]['Error50_arcmin']/60

for i in range(len(iceberg0)):
	event_str =  iceberg0[i]['Event']
	date_str = '{0}/{1}/{2}'.format(event_str[2:4], event_str[4:6], event_str[6:8])
	idx = np.where(ice_EHE0['Date']==date_str)[0]
	if len(idx):
		#print (i, event_str, ice_EHE0[idx]['Signalness'])
		print ('adding  EHE event:',event_str )
		iceberg0[i]['signalness'] = ice_EHE0[idx[0]]['Signalness']
		iceberg0[i]['R50'] = ice_EHE0[idx[0]]['Error']/60

# don't use HESE because they don't have real signalness
# for i in range(len(iceberg0)):
# 	event_str =  iceberg0[i]['Event']
# 	date_str = '{0}/{1}/{2}'.format(event_str[2:4], event_str[4:6], event_str[6:8])
# 	idx = np.where(ice_HESE0['Date']==date_str)[0]
# 	if len(idx):
# 		#print (i, event_str, str(np.array(ice_HESE0[idx]['Date'])), float(ice_HESE0[idx]['Signalness']))
# 		print ('adding  HESE event:',event_str )
# 		iceberg0[i]['signalness'] = ice_HESE0[idx[0]]['Signalness']
# 		iceberg0[i]['R50'] = ice_HESE0[idx[0]]['Error']/60


# remove events for which no signalness was found
# IC200410A has area of 300 sq deg.
igotsignal = (iceberg0['signalness']>0) 
iareacut = (iceberg0['area']<100)
i2021cut = iceberg0['jd']<sjoert.simtime.mjdtojd(sjoert.simtime.yeartomjd(2021))

print ('events w/o signalness         :', iceberg0[igotsignal==False]['Event'])
print ('events too large area         :', iceberg0[iareacut==False]['Event'])
print ('events after 2021        		:', iceberg0[i2021cut==False]['Event'])

iceberg = iceberg0[igotsignal*iareacut*i2021cut]
print ('total number of IceCube events:',len(iceberg))


