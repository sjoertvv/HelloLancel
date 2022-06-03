'''
define global settings for the likelihood anaylsis
'''
settings = dict()

settings['do_twomass'] 	= False 	# if True, sample coordindates from 2MRS; default is to use the KDE of the RA, Decl. of the parent sample of ZTF nuclear flares
settings['do_all_ZTF'] 	= False   	# if True, we make no selection on the optical properties of the flare, simply select all dust echo candidates
settings['do_superEdd'] = False 	# if True, restrict to flares with evidence for super-Edding peak accretion rates
settings['Ntest']		= int(4e5) 	# Number of Monte Carlo samples. 1e5 is fast but not enough, 1e6 is used for publication (if do_twomass==True, 1e6 is overkill, and you can use 1e5)
settings['min_b'] 		= 8 		# Galatic lattitude to define the plane (inside the plane we force zero probability of the KDE)

settings['tdiff_max'] = 365			# time in days post optical peak to allow a neutrino temporal coincidence
settings['tdiff_min'] = 0 			# time in days pre optical peak to allow a neutrino temporal coincidence