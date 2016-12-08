#!/Users/Shrey/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 6, 6

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
df = pd.DataFrame({'Teff': Teff, 'logg': logg, 'mass': mass,\
'Prot': Prot, 'Rper': Rper, 'Fe/H': FeH, 'rad': rad, 'rho': rho})
df.sort_values(by = 'Prot', inplace = True)

def movingmedian(x,window):
    """Calculates a smoothed function for outlier rejection based on a moving median.

    Keyword Arguments:
    x -- a 1d dataset to perform the moving median on
    window -- the number of datapoints to take into account for the median
    """
    down = []
    smoothed = []
    up = []
    i = 0
    while i < len(x)-window:
        dataset = x[i:i+window]
        med = np.median(dataset)
        low = np.percentile(dataset, 5)
        high = np.percentile(dataset, 95)
        down.append(low)
        smoothed.append(med)
        up.append(high)
        i += 1
    return [down, smoothed, up]

window = 2000
down, smooth, up = movingmedian(df['Teff'], window)
plt.plot(df['Prot'][window/2:-window/2], smooth, alpha = 0.5, c = 'b')
plt.plot(df['Prot'][window/2:-window/2], down, alpha = 0.5, c = 'r')
plt.plot(df['Prot'][window/2:-window/2], up, alpha = 0.5,c = 'r')


plt.scatter(Prot, Teff, c = 'k', s = 0.2)
plt.xscale('log')
plt.xlabel(r'P$_{rot}$ [days]')
plt.ylabel(r'T$_{eff}$ [K]')
plt.ylim(3500,7000)
plt.xlim(.2, 90)
plt.savefig(output_dir+"envelope_1", format='png')
print("envelope plot made")
