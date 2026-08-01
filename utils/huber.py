
def huber(z, rho, cost_only):
    mask = z <= 1
    rho[0, mask] = z[mask]
    rho[0, ~mask] = 2 * z[~mask]**0.5 - 1
    if cost_only:
        return
    rho[1, mask] = 1
    rho[1, ~mask] = z[~mask]**-0.5
    rho[2, mask] = 0
    rho[2, ~mask] = -0.5 * z[~mask]**-1.5

