
def _hc(k, cs, rho, omega):
    return (cs / sin(omega) * (rho ** k) * sin(omega * (k + 1)) *
            greater(k, -1))

