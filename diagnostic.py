#!/Users/Shrey/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 7.5, 7.5

output_dir = "simple_plots/"
data = np.genfromtxt("crossref.txt")
Teff = data[:,1]
logg = data[:,2]
mass = data[:,3]
Prot = data[:,4]
Rper = data[:,6]
FeH = data[:,11]
rad = data[:,12]
rho = data[:,13]
L = np.log(((Teff/5780)**4)*(rad**2))

df = pd.DataFrame({'Teff': Teff, 'logg': logg, 'mass': mass,\
'log(Prot)': np.log(Prot), 'log(Rper)': np.log(Rper), 'Fe/H': FeH,\
'rad': rad, 'rho': rho, 'L': L})
ax1 = pd.scatter_matrix(df,s = .2, alpha = 0.2,  diagonal = 'kde')

midmass = np.median(mass)
stdmass = np.std(mass)
midlogg = np.median(logg)
stdlogg = np.std(logg)
midrad = np.median(rad)
stdrad = np.std(rad)
midrho = np.median(rho)
stdrho = np.std(rho)

for i, axs in enumerate(ax1):
    for j, ax in enumerate(axs):
        if i != j and i == 1:
            ax.set_ylim((-3, 1.6))
        if i != j and i == 5:
            ax.set_ylim((midlogg-stdlogg, midlogg+stdlogg))
        if i != j and i == 6:
            ax.set_ylim((0, 1))
        if i != j and i == 7:
            ax.set_ylim((midrad-2*stdrad, midrad+2*stdrad))
        if i != j and i == 8:
            ax.set_ylim((0, midrho+stdrho))
        if j == 1:
            ax.set_xlim((-3,1.6))
        if j == 5:
            ax.set_xlim((midlogg-stdlogg, midlogg+stdlogg))
        if j == 6:
            ax.set_xlim((0, 1))
        if j == 7:
            ax.set_xlim((midrad-2*stdrad, midrad+2*stdrad))
        if j == 8:
            ax.set_xlim((0, midrho+stdrho))

plt.savefig(output_dir+"diagnostic", format='png')
plt.gcf().clear()
print "diagnostic made"
"""
plt.scatter(Prot, Teff, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
plt.ylim(3000,7000)
plt.xlim(0.2, 90)
plt.ylabel(r'T$_{eff}$ [K]')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_Teff", format='png')
plt.gcf().clear()

plt.scatter(Prot, logg, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
#plt.ylim(3000,7000)
plt.xlim(0.2, 90)
plt.ylabel(r'log g')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_logg", format='png')
plt.gcf().clear()


plt.scatter(Prot, mass, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
plt.yscale('log')
#plt.ylim(3000,7000)
plt.xlim(0.2, 90)
plt.ylabel(r'Mass [M$_{sun}$]')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_mass", format='png')
plt.gcf().clear()

plt.scatter(Prot, FeH, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
plt.ylim(-1.5,.7)
plt.xlim(0.2, 90)
plt.ylabel(r'Fe/H')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_FeH", format='png')
plt.gcf().clear()

plt.scatter(Prot, rad, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
#plt.ylim(3000,7000)
plt.xlim(0.2, 90)
plt.ylabel(r'Radius')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_rad", format='png')
plt.gcf().clear()

plt.scatter(Prot, rho, s = 2, alpha = 0.5, color = 'k')
plt.xscale('log')
#plt.ylim(3000,7000)
plt.xlim(0.2, 90)
plt.ylabel(r'Density')
plt.xlabel(r'P$_{rot}$ [days]')
plt.savefig(output_dir+"P_rho", format='png')
"""
