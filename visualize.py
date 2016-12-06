#!/Users/Shrey/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
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
plt.gcf().clear()

