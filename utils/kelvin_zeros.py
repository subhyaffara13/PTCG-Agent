
def kelvin_zeros(nt):
    """Compute `nt` zeros of all Kelvin functions.

    Parameters
    ----------
    nt : int
        Number of zeros to compute for each function.

    Returns
    -------
    zeros : tuple of arrays
        Length-8 tuple of arrays of length `nt`.  The tuple contains the arrays of zeros
        of ``(ber, bei, ker, kei, ber', bei', ker', kei')``.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("nt must be positive integer scalar.")
    return (_specfun.klvnzo(nt, 1),
            _specfun.klvnzo(nt, 2),
            _specfun.klvnzo(nt, 3),
            _specfun.klvnzo(nt, 4),
            _specfun.klvnzo(nt, 5),
            _specfun.klvnzo(nt, 6),
            _specfun.klvnzo(nt, 7),
            _specfun.klvnzo(nt, 8))

