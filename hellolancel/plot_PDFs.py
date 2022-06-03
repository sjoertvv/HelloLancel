'''
this can run after loading TS_input
'''
from hellolancel.TS_input import *
from matplotlib import pyplot as plt

plt.clf()
plt.hist(np.log10(data[flux_check_key][iparent]), bins=140, range=[-7.5,0], cumulative=False,density=True, histtype='step', lw=1.5, ls='-',color=cc_dict['Parent sample'],label='Parent sample')

xx = np.linspace(-5,-1.9, 100)
plt.plot(xx, p_flux_bg(xx), '--', color=cc_dict['Parent sample'], label='P(x|B)')
plt.plot(xx, p_flux_sig(xx), '--', color='purple', label='P(x|S)')
plt.plot(xx, p_flux_sig(xx)/p_flux_bg(xx), '-k', label='$P(x|S)~/~P(x|B)$')
plt.xlabel('$\Delta F_{IR}$ ($log_{10}$ Jy)')
plt.ylabel('Probability density/ratio')
plt.yscale('log')
plt.yscale('log')
plt.ylim(4e-3, 450)
plt.xlim(-4.0, -1.8)
plt.legend()
plt.pause(0.1)
key = input('next?')


plt.clf()
xx_plt = np.linspace(0,2)
bin_min = 0.5
strength_use = np.log10(data['df_over_rms'])
plt.hist(strength_use[iac*itde], bins=30,range=[bin_min,2], cumulative=False,density=True, histtype='step', lw=2., ls='-',color=cc_dict['TDE'],label='TDEs + candidates')
plt.hist(strength_use[iac*inottde], bins=30, range=[bin_min,2], cumulative=False,density=True, histtype='step', lw=1.5, ls='-',color=cc_dict['Parent sample'],label='Accretion flares w/o TDEs')
plt.plot(xx_plt, p_strength_bg(xx_plt),'--',color=cc_dict['Parent sample'],  label='P(x|B)')
plt.plot(xx_plt, p_strength_sig(xx_plt),'--',color=cc_dict['TDE'],  label=r'P(x|S)')
plt.plot(xx_plt, p_strength_sig(xx_plt)/p_strength_bg(xx_plt),'-k',  label=r'P(x|S) / P(x|B)')
plt.ylabel('Probability density/ratio')
plt.xlabel('Dust echo strength ($log_{10}\, \\Delta F_{IR} / F_{rms}$)')
plt.yscale('log')
plt.ylim(0.2, 15)
plt.xlim(0.5, 2.02)
plt.legend(loc=2)
plt.pause(0.1)
key = input('next?')