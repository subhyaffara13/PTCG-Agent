
def _hs(k, cs, rho, omega):
    c0 = (cs * cs * (1 + rho * rho) / (1 - rho * rho) /
          (1 - 2 * rho * rho * cos(2 * omega) + rho ** 4))
    gamma = (1 - rho * rho) / (1 + rho * rho) / tan(omega)
    ak = abs(k)
    return c0 * rho ** ak * (cos(omega * ak) + gamma * sin(omega * ak))

