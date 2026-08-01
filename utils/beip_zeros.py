
def beip_zeros(nt):
    """Compute nt zeros of the derivative of the Kelvin function bei.

    Parameters
    ----------
    nt : int
        Number of zeros to compute. Must be positive.

    Returns
    -------
    ndarray
        First `nt` zeros of the derivative of the Kelvin function.

    See Also
    --------
    bei, beip

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("nt must be positive integer scalar.")
    return _specfun.klvnzo(nt, 6)

