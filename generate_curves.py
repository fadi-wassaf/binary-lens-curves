from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('ggplot')

# This function returns the roots for the critical curve polynomial for a given value of phi
def crit_poly_coeffs(phi, z1, z2):
    return [np.exp(1j*phi), np.exp(1j*phi)*(-2*z1-2*z2), np.exp(1j*phi)*(4*z1*z2 + z1**2 + z2**2) - 1,
            np.exp(1j*phi)*(-2*z1**2*z2 - 2*z1*z2**2), np.exp(1j*phi)*z1**2*z2**2 + z1*z2]

# This function maps a coordinate in the lens plane to the source plane
# using the binary lens equation in complex coordinates.
def crit_to_caustic(z, z1, z2):
    return z - m1/(z.conj() - z1) - m2/(z.conj() - z2)

# Format is: m1, d, letter 
# (Later I use that m1 + m2 = 1. This generalization was made to derive the polynomial above)
lens_systems = [(.5, 2), (.9, 1.1), (.95, .8), (.75, 1.2)]

# Generate graph of critical and caustic curves for each lens system above
graph = 1
for LS in lens_systems:
    
    plt.figure(graph, figsize=(6,4))
    
    # Get m1 and m2
    m1 = LS[0]
    m2 = 1 - m1
    
    # Get z1 and z2 using the equations given
    d = LS[1]
    z1_ = -m1 * d
    z2_ = m2 * d

    # Get the x center of mass to be used later for shifting the curves
    xcom = z1_*m1 + z2_*m2
    
    # Find the roots of the polynomial for phi 0 to 4 pi
    phi_range = np.linspace(0, 4*pi, 5000)
    roots = [np.roots(crit_poly_coeffs(p, z1_, z2_)) for p in phi_range]

    # Extract the x and y coordinates of the critical curve from the roots
    # Also at the same time convert the critical curve points to the caustic curve points
    crit_x = np.array([])
    crit_y = np.array([])
    caustic_x = np.array([])
    caustic_y = np.array([])
    for rs in roots:
        for i in range(0, 4):
            crit_x = np.append(crit_x, rs[i].real)
            crit_y = np.append(-crit_y, rs[i].imag)
            zs = crit_to_caustic(rs[i], z1_, z2_)
            caustic_x = np.append(caustic_x, zs.real)
            caustic_y = np.append(caustic_y, zs.imag)

    # Plot the (shifted) critical and caustic curves
    plt.scatter(crit_x - xcom, crit_y, s=.1)
    plt.scatter(caustic_x - xcom, caustic_y, s=.1)    
    
    # Plot the locations of z1, z2 and the center of mass
    plt.plot(0, 0, marker='x', c='k', label="COM")
    plt.plot(z1_ - xcom, 0, marker='o', c='r', label="z1")
    plt.plot(z2_ - xcom, 0, marker='o', c='g', label="z2")
    
    # Add legend and title
    plt.title('m1 = %.6g, d = %.3g' % (m1, d) )
    plt.legend()
    plt.savefig('./imgs/m1_%.6g_d_%.3g.png' % (m1, d), dpi=300)
    
    graph += 1