
def _cdf_single_value_piecewise_Z1(x, alpha, beta, **kwds):
    # convert from Nolan's S_1 (aka S) to S_0 (aka Zolaterev M)
    # parameterization

    zeta = -beta * np.tan(np.pi * alpha / 2.0)
    x0 = x + zeta if alpha != 1 else x

    return _cdf_single_value_piecewise_Z0(x0, alpha, beta, **kwds)

