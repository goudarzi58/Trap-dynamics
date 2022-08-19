###

"""
This program is written for simulating the spectral nature
of capture and emission time constants of plasmonic hot electrons
generated by the plasmon decay in metal when being trapped in a
interface state or a border trap

"""
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
lambada_LRP = (lambada/n_LRP)*(1/0.05291772490001)
A = 25* (lambada_LRP**2) #### Length of the film is 5 times of LRP wavelength in a.u.
dt = 0.6 *(1/0.05291772490001) ### in a.u.
dd = 1.2* (lambada/(2*np.pi*np.sqrt(n_LRP**2 - epsd**2)))
print('dd', dd)
#################  Voltage ####################
### Dielectric Sterength of SiO2 = 10**7 V/cm = 10 V/nm = 
epsr_SiO2 = 3.7
e0 = 1.602e-19
def phib(vol):
    phiB = Ec_ox -  Hartree*np.sqrt((e0*vol)/((4*np.pi*8.854*1e-12)*dd*1e-9*epsr_SiO2))
    
    return phiB
phib = np.vectorize(phib)
phiB = phib(0)
N0e0 = np.array([1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
Ne0 = N0e0*(1e21)*((0.05291772490001)**3)

# ###Input data
T = np.array([90, 150, 300])
kT = kb*T  ### the thermal energy in eV
Ehot = 1.8 *Hartree ## the energy of hot-electron in eV
E_T = 1*Hartree ## the trap level in eV
px = np.sqrt(m_Au*Ehot*np.sin(theta_in))/h_bar ### to simplify the calculations
py=px    ### to simplify the calculations

### ===>> Ehot_parl = Ehot* np.sin(theta_in[0])**2  ###not sure if it should be used
E_parl = kT   ### Parralel energy# it ommites 
##print('kT', kT)
h_omegap = 20*1e-3*Hartree  #Boltzman constant in eV/K ## The phonon energy in eV
S = 60   ###  HR-factor
Wmp = {i:[] for i in range(len(T))}
T0p = {i:[] for i in range(len(T))}
for i in range(len(T)):
    tp = np.zeros((Ne0.shape[0]))
##    print('wmp', wmp)
    for j in range(Ne0.shape[0]):
 
        deltaE = Ehot-E_T
        #print('deltaE:', deltaE)
        px = np.sqrt(m_Au*Ehot*np.cos(theta_in))/h_bar ### to simplify the calculations
        py=px    ### to simplify the calculations

    #   ### The number of emitted phonons of energy h_omega in the transition
    #   ### of a hot_e with energy of Ehot into the trap of E_T
        P_Eh = np.round(((deltaE)+E_parl[i])/h_omegap)
        n_occ = 1/(np.exp(h_omegap/kT[i]))  #   ### the phonon occupation function
    #   ### xi factor
        xi = 2*S* np.sqrt(n_occ * (n_occ+1))
    #   ### chi factor
        chi = (P_Eh)**2 + xi**2
        xx = np.float_power((1/5), 2)
    #   ### The auxilary function

        G_deltaE = (1/(np.sqrt(2*np.pi)*h_omegap))*(np.float_power(1/chi, 0.25))*(
                np.float_power(xi/(P_Eh + np.sqrt(chi)), P_Eh)) *(
                np.exp(np.sqrt(chi) - (2*n_occ+1)*S + (P_Eh*h_omegap)/2*kT[i]))

        
        # ## Calculating the trap activation energy
        E_B = (Ehot - E_T - S*h_omegap)**2/(4*S*h_omegap)  ## Trap thermal barrier energy
        # ## The Relaxation energy (should be calculated from S and h_omegap)
        E_rlx = (E_T + S*h_omegap)**2/(4*S*h_omegap)
        # ### redius of solid sphere shape defect in Oxide
        R_T = (0.5*h_bar)/np.sqrt(2*m_ox*(Ec_ox-E_T))
        a_T = 1.612 * R_T   ### This the side length of the cube that surround the spher
        V_T = a_T**3  ## The volume of trap
        # ### Building the wave function of tunneling hot electron from metal to oxide
        p_rel = np.sqrt(2*m_ox*(phiB - Ehot)/h_bar**2) ## the extra momentum that an electron needs to reach Ec of oxide and be considered free

        pz = np.sqrt(m_Au*Ehot*np.cos(theta_in))/h_bar
        ### H_e in the paper: This the damping factor for WF of the electron
        p_dmp = np.sqrt(p_rel**2+px**2+py**2) # ### kx and ky are the in plane momentums of the tunneling elecron inside the oxide
        ### The integral parameters:
        q_xm = np.sqrt(2)/(2*R_T)
        q_zm = q_xm
        deltax = 2*q_xm/2000
        qx = np.linspace(-q_xm, q_xm+deltax, num=2000)
        ##print('qx:', qx)
        deltaz = 2*q_xm/2000
        qz = np.linspace(-q_zm, q_zm+deltaz, num=2000)
        ##print('qz:', qz)
        ##########################################
      
        def I_px(qx):
            return abs(2*np.sin(0.5*(px+qx)*a_T)/(px+qx))**2
        I_px = np.vectorize(I_px)
        i_px = np.sum(I_px(qx))*deltax


        # #########

        def I_pz(qz):
            return abs(2j*np.sin((1j*(pz+qz)-p_dmp)*a_T/2)/(1j*(pz+qz)-p_dmp))**2
        I_pz = np.vectorize(I_pz)
        i_pz = np.sum(I_pz(qz))*deltaz
        ############################################

        def I_x(qx):
            return abs(2*np.sin(0.5*qx*a_T)/qx)**2
        I_x = np.vectorize(I_x)
        i_x = np.sum(I_x(qx))*deltax
        ##### #########
        def I_z(qz):
            return abs(2*np.sin(0.5*qz*a_T)/qz)**2
        I_z = np.vectorize(I_z)
        i_z = np.sum(I_z(qz))*deltaz
        ############################################

        ### #################
        c1 = 2*(pz**2/(p_dmp**2+pz**2))
        c2 = 2*(V_T*(h_omegap**2)/A)
        ### The transfer matrix element
        Tm = S*c1*c2*np.exp(-1*p_dmp*dt)*((i_px*i_pz)/(i_x*i_z))
##      print('Tm:', Tm)
        Wmp_Eh = (np.pi/h_bar)*S*Tm*((1-(P_Eh/S))**2)*G_deltaE
##        print('Wmp_Eh', Wmp_Eh)
        
        c_Eh = Wmp_Eh * A
##        print('c_Eh', c_Eh)
        ### The hot-electron concentration per unit area having the minemum required


##        print('Ne0:', Ne0)
        t0p = 1/(c_Eh*Ne0[j])
        tp[j] = t0p
##    print('wmp', wmp)
    T0p[i] =  tp 
print('T0p', T0p)
##print('T0p', T0p[0])
##print('T0p', T0p[0])
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



for i in range(1):
    plt.plot(N0e0 , T0p[i+2], color=colors[i], linewidth=3, ls=Ls[i])
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
        

plt.xlabel('Hot-electron  concentration ($cm^{-3}$)', labelparams)
##plt.xlim([0, 6.8])
##plt.ylim(1e-24, 1e-12)
plt.ylabel('trap time (s)', labelparams)
mpl.rcParams.update({'font.size': 12})#, {'font.weight': 'bold'})
###plt.legend(loc='lower center')
plt.rcParams['axes.labelweight'] = "bold"
plt.rcParams["font.weight"] = "bold"
##plt.legend(title = "$E_{hote}=1.8eV$, $E_T=1eV$, $d_T=0.6nm$  T=300K,")


#plt.rcParams['title.labelweight'] = 'bold'
##plt.title('Trap time vs Hot electron  concentration',fontweight="bold", fontsize=16)

plt.show()