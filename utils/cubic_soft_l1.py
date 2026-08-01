
def cubic_soft_l1(z):
    rho = np.empty((3, z.size))

    t = 1 + z
    rho[0] = 3 * (t**(1/3) - 1)
    rho[1] = t ** (-2/3)
    rho[2] = -2/3 * t**(-5/3)

    return rho

