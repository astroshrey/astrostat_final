#!/Users/Shrey/anaconda2/bin/python

##########################################
#Shreyas Vissapragada
#sv2421
#Creating the diagnostic plot matrix
#for further inspection for trends
##########################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 7.5, 7.5

#reading in data from the cross-refd dataset
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
L = np.log(((Teff/5780)**4)*(rad**2)) #calculated parameter

df = pd.DataFrame({'Teff': Teff, 'logg': logg, 'mass': mass,\
'log(Prot)': np.log(Prot), 'log(Rper)': np.log(Rper), 'Fe/H': FeH,\
'rad': rad, 'rho': rho, 'L': L})

#making the plot matrix
ax1 = pd.scatter_matrix(df,s = .2, alpha = 0.2,  diagonal = 'kde')


#from here on out this is just messing around with plt to set plotting limits

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

plt.savefig(output_dir+"diagnostic.png", format='png')
