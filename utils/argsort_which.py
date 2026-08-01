
def argsort_which(eigenvalues, typ, k, which,
                  sigma=None, OPpart=None, mode=None):
    """Return sorted indices of eigenvalues using the "which" keyword
    from eigs and eigsh"""
    if sigma is None:
        reval = np.round(eigenvalues, decimals=_ndigits[typ])
    else:
        if mode is None or mode == 'normal':
            if OPpart is None:
                reval = 1. / (eigenvalues - sigma)
            elif OPpart == 'r':
                reval = 0.5 * (1. / (eigenvalues - sigma)
                               + 1. / (eigenvalues - np.conj(sigma)))
            elif OPpart == 'i':
                reval = -0.5j * (1. / (eigenvalues - sigma)
                                 - 1. / (eigenvalues - np.conj(sigma)))
        elif mode == 'cayley':
            reval = (eigenvalues + sigma) / (eigenvalues - sigma)
        elif mode == 'buckling':
            reval = eigenvalues / (eigenvalues - sigma)
        else:
            raise ValueError(f"mode='{mode}' not recognized")

        reval = np.round(reval, decimals=_ndigits[typ])

    if which in ['LM', 'SM']:
        ind = np.argsort(abs(reval))
    elif which in ['LR', 'SR', 'LA', 'SA', 'BE']:
        ind = np.argsort(np.real(reval))
    elif which in ['LI', 'SI']:
        # for LI,SI ARPACK returns largest,smallest abs(imaginary) why?
        if typ.islower():
            ind = np.argsort(abs(np.imag(reval)))
        else:
            ind = np.argsort(np.imag(reval))
    else:
        raise ValueError(f"which='{which}' is unrecognized")

    if which in ['LM', 'LA', 'LR', 'LI']:
        return ind[-k:]
    elif which in ['SM', 'SA', 'SR', 'SI']:
        return ind[:k]
    elif which == 'BE':
        return np.concatenate((ind[:k//2], ind[k//2-k:]))

