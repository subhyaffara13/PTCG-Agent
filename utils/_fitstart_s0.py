
def _fitstart_S0(data):
    alpha, beta, delta1, gamma = _fitstart_S1(data)

    # Formulas for mapping parameters in S1 parameterization to
    # those in S0 parameterization can be found in [NO]. Note that
    # only delta changes.
    if alpha != 1:
        delta0 = delta1 + beta * gamma * np.tan(np.pi * alpha / 2.0)
    else:
        delta0 = delta1 + 2 * beta * gamma * np.log(gamma) / np.pi

    return alpha, beta, delta0, gamma

