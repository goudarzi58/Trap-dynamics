 #---- Plot Hot_e and Hot_h Histograms
import numpy as np
import matplotlib.pyplot as plt
import operator
from scipy.io import loadmat
import matplotlib.pyplot as plt
import scipy.stats as ss

# Loading Hot_e and Hot_h
eV = 1. / 27.21138386
Ee = np.array(list(np.load('SRP_E_e_angle.npy')))/ eV
Eh = np.array(list(np.load('SRP_E_h_angle.npy')))/ eV
weights = np.array(list(np.load('weights_LRP_angle.npy')))
##mu, sigma = 100, 15

# the histogram of the data
nBins = 200
##plt.hist(e_outData[:,0],nBins, weights=e_outData[:,1], density=True, facecolor='r')
plt.hist(Ee,nBins, weights=weights, normed=1, histtype='step', lw=2, color='red')
##normed=1, histtype=’step’, lw=2, color=’red’

##fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8.27, 11.69))
##axes.hist((e_outData[1]),nBins, histtype='stepfilled', density=True, color='green', label='Hello world!', alpha=0.70)
####e_hist,e_binEdges = plt.hist(e_outData[:,0], e_outData[:,1], density=True, facecolor='r')
##data = [cs.Bar(x=e_outData[:,0], y=e_outData[:,1])]
##py.plot(data, filename='bar-histogram')
##n, bins, patches = plt.hist(x, 50, density=True, facecolor='r', alpha=0.75)
##
##
plt.xlabel('Energy')
plt.ylabel('Weight')
plt.title('Histogram of Hot_e')
##plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
##plt.xlim(40, 160)
##plt.ylim(0, 0.03)
##plt.grid(False)
plt.show()
plt.savefig('hist.jpg', dpi=1000)



