
def _maybe_real(A, B, tol=None):
    """
    Return either B or the real part of B, depending on properties of A and B.

    The motivation is that B has been computed as a complicated function of A,
    and B may be perturbed by negligible imaginary components.
    If A is real and B is complex with small imaginary components,
    then return a real copy of B.  The assumption in that case would be that
    the imaginary components of B are numerical artifacts.

    Parameters
    ----------
    A : ndarray
        Input array whose type is to be checked as real vs. complex.
    B : ndarray
        Array to be returned, possibly without its imaginary part.
    tol : float
        Absolute tolerance.

    Returns
    -------
    out : real or complex array
        Either the input array B or only the real part of the input array B.

    """
    # Note that booleans and integers compare as real.
    if np.isrealobj(A) and np.iscomplexobj(B):
        if tol is None:
            tol = {0: feps*1e3, 1: eps*1e6}[_array_precision[B.dtype.char]]
        if np.allclose(B.imag, 0.0, atol=tol):
            B = B.real
    return B

