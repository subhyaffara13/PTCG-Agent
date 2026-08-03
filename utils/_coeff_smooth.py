import math


def _coeff_smooth(lam):
    xi = 1 - 96 * lam + 24 * lam * math.sqrt(3 + 144 * lam)
    omeg = math.atan2(math.sqrt(144 * lam - 1), math.sqrt(xi))
    rho = (24 * lam - 1 - math.sqrt(xi)) / (24 * lam)
    rho = rho * math.sqrt((48 * lam + 24 * lam * math.sqrt(3 + 144 * lam)) / xi)
    return rho, omeg

