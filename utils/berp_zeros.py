
def berp_zeros(nt):
    """Compute nt zeros of the derivative of the Kelvin function ber.

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
    ber, berp

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html


    Examples
    --------
    Compute the first 5 zeros of the derivative of the Kelvin function.

    >>> from scipy.special import berp_zeros
    >>> berp_zeros(5)
    array([ 6.03871081, 10.51364251, 14.96844542, 19.41757493, 23.86430432])

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("nt must be positive integer scalar.")
    return _specfun.klvnzo(nt, 5)

