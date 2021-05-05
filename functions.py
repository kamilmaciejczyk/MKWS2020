import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

npoints = 50

gas = ct.Solution('gri30.xml')

# HP - adiabatic
# SV - with constant volume

equivalence_ratio_H2 = 'H2:1.0'
equivalence_ratio_O2_N2 = 'O2:0.5, N2:1.88'

phi = [0.5, 1, 2, 3, 4] 

tad05 = np.zeros(npoints)
tad1 = np.zeros(npoints)
tad2 = np.zeros(npoints)
tad3 = np.zeros(npoints)
tad4 = np.zeros(npoints)

tad = [tad05, tad1, tad2, tad3, tad4] 



def tempForDifferentPressures(equlibrium, T0):
    P = np.linspace(0.1*ct.one_atm, ct.one_atm*5, npoints)

    yLabelText = 'Adiabatic flame temperature [K]' if equlibrium == "HP" else 'Const. volume flame temperature [K]'

    for j in range(len(phi)):
        for i in range(npoints):
            gas.TP = T0, P[i]
            gas.set_equivalence_ratio(phi[j], equivalence_ratio_H2, equivalence_ratio_O2_N2)
            gas.equilibrate(equlibrium)
            tad[j][i] = gas.T

    fig, ax = plt.subplots()

    for j in range(len(phi)):
        plt.plot(P/100000, tad[j], label = '$ \Phi$ = ' + str(phi[j]))
        
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set(xlabel = 'Initial pressure [bar]', ylabel = yLabelText)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.savefig('plots/temp_for_diff_press_for_' + equlibrium)

    return plt 



def tempForDifferentInitTemp(equlibrium, P0):
    T = np.linspace(273, 2000, npoints)

    yLabelText = 'Adiabatic flame temperature [K]' if equlibrium == "HP" else 'Const. volume flame temperature [K]'

    for j in range(len(phi)):
        for i in range(npoints):
            gas.TP = T[i], P0
            gas.set_equivalence_ratio(phi[j], equivalence_ratio_H2, equivalence_ratio_O2_N2)
            gas.equilibrate(equlibrium)
            tad[j][i] = gas.T

    fig, ax = plt.subplots()

    for j in range(len(phi)):
        plt.plot(T, tad[j], label = '$ \Phi$ = ' + str(phi[j]))
        
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set(xlabel = 'Initial temperature [K]', ylabel = yLabelText)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.savefig('plots/temp_for_diff_init_temp_for_' + equlibrium)

    return plt 


def tempForPhi(phi, equilibrium):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    temp = np.zeros( (npoints, npoints) )

    t = np.linspace(273, 2000, npoints)
    p = np.linspace(0.1*ct.one_atm, ct.one_atm*5, npoints)

    T, P = np.meshgrid(t, p)

    for i in range(npoints):
        for j in range(npoints):
            gas.TP = t[i], p[j]
            gas.set_equivalence_ratio(phi, equivalence_ratio_H2, equivalence_ratio_O2_N2)
            gas.equilibrate(equilibrium)
            temp[j][i] = gas.T

    # Make data.

    # Plot the surface.
    surf = ax.plot_surface(P / 100000, T, temp, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.0f}')
    ax.set(ylabel = 'Initial temperature [K]', xlabel = "Initial pressure [bar]")

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    label = 'Adiabatic flame temperature [K]' if equilibrium == "HP" else 'Const. volume flame temperature [K]'

    fig.suptitle(label + ' for $ \Phi$ = ' + str(phi))

    plt.savefig('plots/3d_plot_for_phi=' + str(phi) + '_' + equilibrium + '.png')

    return plt