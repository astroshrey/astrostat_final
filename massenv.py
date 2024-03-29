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
L = np.log(((Teff/5780)**4)*(rad**2))
df = pd.DataFrame({'Teff': Teff, 'logg': logg, 'mass': mass,\
'Prot': Prot, 'Rper': Rper, 'Fe/H': FeH, 'rad': rad, 'rho': rho, 'L': L})
df.sort_values(by = "Prot", inplace = True)
df= df[df["Prot"] < 50]

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
down, smooth, up = movingmedian(df['mass'], window)
x = np.array(df['Prot'][window/2:-window/2])
print min(x), max(x)
plt.plot(x, smooth, alpha = 0.5, c = 'y')
plt.plot(x, down, alpha = 0.5, c = 'r')
plt.plot(x, up, alpha = 0.5,c = 'r')


plt.scatter(df['Prot'], df['mass'], c = 'k', s = 0.2)
plt.xscale('log')
plt.xlabel(r'P$_{rot}$ [days]')
plt.ylabel(r'M/M$_{\odot}$')
plt.ylim(0.1, 1)
plt.xlim(min(x), max(x))
plt.savefig(output_dir+"envelope_5.png", format='png')
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

def k_folds(data,k, to_plot = False):
    """k-folds cross-validation function. The dataset is randomly shuffled
    and chunked into k nearly-equal chunks of size floor(len(dat)/k). I say
    nearly-equal because the final chunk will pick up any remaining points; for
    instance, a 5-fold of the 241 point dataset will have 48,48,48,48,49 points
    in each validation set. Again the actual cross validation work is
    done by cross_validate above. This function returns the average
    chi-squared over all k folds.

    Keyword Arguments:
    k -- the number of folds
    to_plot -- whether or not to plot the models on the data.

    Note: the models actually look *really* messy and I haven't
    figured out a way to make it look nice given the large volume
    of data, so I have set the default for to_plot to false.
    """

    i = 0
    chunk_size = len(data)/k
    num_chunks = 0
    summed = np.array([0.0,0.0,0.0,0.0])

    while i < len(data):
        #the following if-statement is to cover the edge case of the
        #last bucket picking up remaining points.
        if len(data) - i < 2*chunk_size:
            dataval = data[i:]
            datatra = data[:i]
            xtra = np.array(datatra[:,0].T)[0]
            ytra = np.array(datatra[:,1].T)[0]
            xval = np.array(dataval[:,0].T)[0]
            yval = np.array(dataval[:,1].T)[0]
            summed += cross_validate(xtra, ytra, xval, yval, to_plot)
            num_chunks += 1
            break

        else:
            dataval = data[i:i+chunk_size]
            datatra = np.vstack((data[:i],data[i+chunk_size:]))
            xtra = np.array(datatra[:,0].T)[0]
            ytra = np.array(datatra[:,1].T)[0]
            xval = np.array(dataval[:,0].T)[0]
            yval = np.array(dataval[:,1].T)[0]
            summed += cross_validate(xtra, ytra, xval, yval, to_plot)
            i += len(data)/k
            num_chunks += 1
    x = np.array(data[:,0].T)[0]
    y = np.array(data[:,1].T)[0]

    models = [np.poly1d(np.polyfit(x, y, deg = 0)) \
    , np.poly1d(np.polyfit(x, y, deg = 1)) \
    , np.poly1d(np.polyfit(x, y, deg = 2)) \
    , np.poly1d(np.polyfit(x, y, deg = 3))]
    avg = summed/num_chunks
    print avg
    return models[2]

data = np.transpose(np.matrix([x,up]))
print k_folds(data, 100)

data = np.transpose(np.matrix([x,down]))
print k_folds(data, 100)
