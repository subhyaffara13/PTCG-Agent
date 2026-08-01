
def sinhm(A):
    """
    Compute the hyperbolic matrix sine.

    This routine uses expm to compute the matrix exponentials.

    Parameters
    ----------
    A : (N, N) array_like
        Input array.

    Returns
    -------
    sinhm : (N, N) ndarray
        Hyperbolic matrix sine of `A`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import tanhm, sinhm, coshm
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> s = sinhm(a)
    >>> s
    array([[ 10.57300653,  39.28826594],
           [ 13.09608865,  49.86127247]])

    Verify tanhm(a) = sinhm(a).dot(inv(coshm(a)))

    >>> t = tanhm(a)
    >>> c = coshm(a)
    >>> t - s.dot(np.linalg.inv(c))
    array([[  2.72004641e-15,   4.55191440e-15],
           [  0.00000000e+00,  -5.55111512e-16]])

    """
    A = _asarray_square(A)
    return _maybe_real(A, 0.5 * (expm(A) - expm(-A)))

