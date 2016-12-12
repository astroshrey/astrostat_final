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
df= df[df["Prot"] < 40]

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
x = np.array(df['Prot'][window/2:-window/2])
plt.plot(x, smooth, alpha = 0.5, c = 'b')
plt.plot(x, down, alpha = 0.5, c = 'r')
plt.plot(x, up, alpha = 0.5,c = 'r')


plt.scatter(df['Prot'], df['Teff'], c = 'k', s = 0.2)
plt.xscale('log')
plt.xlabel(r'P$_{rot}$ [days]')
plt.ylabel(r'T$_{eff}$ [K]')
plt.ylim(3500,7000)
plt.xlim(.2, 90)
plt.savefig(output_dir+"envelope_1", format='png')
print("envelope plot made")


#We can first write a generic cross-validation function that uses a
#chisquared helper function

def chisquared(res,err):
    """Calculates the chi^2 for given residuals and errors.
    This is a helper function for cross_validate below.

    Keyword Arguments:
    res -- the residuals
    err -- the errors
    """
    chi2 = 0.0
    for i in range(len(res)):
        chi2 += (res[i]/err[i])**2
    return chi2

def cross_validate(xtra,ytra,xval,yval, to_plot = False):
    """Trains 0th order, 1st order, 2nd order, and 3rd order polynomials
        on training data, checks them against validation data, and returns
        a 4-element array containing the chi^2 for each model.

    Keyword Arguments:
    xtra -- the x training dataset
    ytra -- the y training dataset
    xval -- the x validation dataset
    yval -- the y validation dataset
    to_plot -- whether or not to plot the models on the data.

    """
    ##training each model##
    M0 = np.poly1d(np.polyfit(xtra, ytra, deg = 0))
    M1 = np.poly1d(np.polyfit(xtra, ytra, deg = 1))
    M2 = np.poly1d(np.polyfit(xtra, ytra, deg = 2))
    M3 = np.poly1d(np.polyfit(xtra, ytra, deg = 3))

    ##validating each model by finding chi2##
    residuals0 = [yval[i] - M0(xval[i]) for i in range(len(xval))]
    residuals1 = [yval[i] - M1(xval[i]) for i in range(len(xval))]
    residuals2 = [yval[i] - M2(xval[i]) for i in range(len(xval))]
    residuals3 = [yval[i] - M3(xval[i]) for i in range(len(xval))]

    #plotting
    if to_plot:
        allx = np.array(sorted(list(xval) + list(xtra)))
        fn0 = [M0(val) for val in allx]
        fn1 = [M1(val) for val in allx]
        fn2 = [M2(val) for val in allx]
        fn3 = [M3(val) for val in allx]

        plt.gcf().clear()
        plt.scatter(xval, yval, color='r')
        plt.scatter(xtra, ytra, color='b')
        plt.plot(x, fn0, color = 'g', ls = ':', lw = 4, label = 'Model 0')
        plt.plot(x, fn1, color = 'g', ls = '-.', label = 'Model 1')
        plt.plot(x, fn2, color = 'g', ls = '--', label = 'Model 2')
        plt.plot(x, fn3, color = 'g', ls = '-', label = 'Model 3')
        plt.xscale('log')
        plt.xlabel(r'P$_{rot}$ [days]')
        plt.ylabel(r'T$_{eff}$ [K]')
        plt.ylim(3500,7000)
        plt.xlim(.2, 90)
        plt.legend()
        plt.show()



    #getting our chi-squares
    return np.array([chisquared(residuals0, yval),\
            chisquared(residuals1, yval),\
            chisquared(residuals2, yval),\
            chisquared(residuals3, yval)])

print cross_validate(x[200:], up[200:], x[:200], up[:200], to_plot = True)
