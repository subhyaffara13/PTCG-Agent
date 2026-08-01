
def soft_l1(z, rho, cost_only):
    t = 1 + z
    rho[0] = 2 * (t**0.5 - 1)
    if cost_only:
        return
    rho[1] = t**-0.5
    rho[2] = -0.5 * t**-1.5

