
def obl_cv_seq(m, n, c):
    """Characteristic values for oblate spheroidal wave functions.

    Compute a sequence of characteristic values for the oblate
    spheroidal wave functions for mode m and n'=m..n and spheroidal
    parameter c.

    Parameters
    ----------
    m, n : int
        Non-negative mode parameters.
    c : float
        Spheroidal parameter.

    Returns
    -------
    cv : array of floats
        Characteristic values.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    """
    if not (isscalar(m) and isscalar(n) and isscalar(c)):
        raise ValueError("Arguments must be scalars.")
    if (n != floor(n)) or (m != floor(m)):
        raise ValueError("Modes must be integers.")
    if (n-m > 199):
        raise ValueError("Difference between n and m is too large.")
    maxL = n-m+1
    return _specfun.segv(m, n, c, -1)[1][:maxL]

