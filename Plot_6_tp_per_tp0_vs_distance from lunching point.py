
import numpy as np
import scipy as sp
import matplotlib.pylab as plt
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
#  ### Constant Values

#h_bar = 6.5821 * 10-16 ## in eV.s
h_bar = 1  ## in atomic Units
##h_bar = 1  ### in a.u.

nm = 0.0529177
Hartree = 1/27.2114
kb = (8.617333262145*1e-5)*Hartree  #Boltzman constant in Hartree/K
#### The Fermi level is the reference
Ec_ox = 4.3*Hartree ## Potential barrier for electrons related to the Fermi level of the gold and in eV
phiB = Ec_ox
Ev_ox = 4.7*Hartree ## Potential barrier for holes related to the Fermi level of the gold and in eV
Eg_ox = 9*Hartree ## Band gap OF SiO2 in eV
Ecnl_ox =-0.2*Hartree # Ev+4.5 ## Charge neutrality level in eV 
m_Au = 1.1 # ## effective mass of e in Au in atomic units (in atomic units)
m_ox = 0.42 # ## effective mass of e in SiO2 (in atomic units)
lambada = 425  ## nm
dm = 15*(1/0.05291772490001) ### the thickness of Au film in nm
epsd = 2.1704
epsm = np.complex(-1.6954, 5.6710) ### it is 
# We asume that all
theta_max = 1  ### ????+
##theta_in = np.array([0, np.pi/36, np.pi/18, np.pi/12, np.pi/9, np.pi/6, np.pi/4, np.pi/3])
##phi_in =
theta_in = 0
#######################:::: Area:
### n_LRP from ref[73]:
def nlrp(x):
    n_LRP = np.sqrt(epsd + (((np.pi*x)/(lambada*epsm))*(epsd-epsm)*epsd)**2)
    return n_LRP
n_LRP = nlrp(dm).real
lambada_LRP = lambada/n_LRP
print('5*lambada_LRP:', 5*lambada_LRP)
Bettaprim = (2*np.pi/lambada)*nlrp(dm).imag
print("Bettaprim:", Bettaprim)
#### dapming coefficient 
def expon(x):
    return np.exp(2*Bettaprim*d)
expon = np.vectorize(expon)
d = np.linspace(0, 5*lambada_LRP, 200)
print("d", d)
dampf = np.exp(-2*Bettaprim*d)
print('dampf:', dampf)
print('$L=5\u03BB_{LRP}$')
#################################### Plot ##########################
from matplotlib import rc,rcParams
from pylab import *


rc('axes', linewidth=3)
rc('font', weight='bold')
rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
fontsize = 18
labelparams = {'size': 20, 'weight':'semibold',
              'family':'serif', 'style':'italic'}
dt = ['$d_t = 0.2 nm$', '$d_t = 0.6 nm$', '$d_t = 1.2 nm$']
Ls = ['--', '-.', ':', '-', '--', '--', '-.', ':', '-', '--',
      '--', '-.', ':', '-', '--', ':', '-.']  
#
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown',
          'pink', 'gray', 'olive', 'darkorange', 'forestgreen', 'navy','seagreen', 'lime', 'peru', 'darkred', 'yellow']

        
plt.plot(d , np.exp(2*Bettaprim*d), color=colors[0], linewidth=3, ls=Ls[0])
ax=plt.gca()
ax.xaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.set_yscale('log')
ax.set_xscale('log')
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
##
####plt.xlim([0, 6.8])
####plt.ylim(1e-24, 1e-12)
plt.xlabel('distance from the lunching point (nm)', labelparams)
plt.ylabel('$T_p/T_{p0}$', labelparams)
##mpl.rcParams.update({'font.size': 12})#, {'font.weight': 'bold'})
#####plt.legend(loc='lower center')
##plt.rcParams['axes.labelweight'] = "bold"
##plt.rcParams["font.weight"] = "bold"
plt.legend(title = "$T_p$ = $T_{p0}$ exp(  2Im(\u03B2)x )", fontsize=10)
           ####plt.rcParams['title.labelweight'] = 'bold'
##plt.title('$W_{mp}$ vs Voltage (T=300K)',fontweight="bold", fontsize=16)
##
plt.show()
#



## in a.u.
