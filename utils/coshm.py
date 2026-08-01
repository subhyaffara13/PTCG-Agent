
def coshm(A):
    """
    Compute the hyperbolic matrix cosine.

    This routine uses expm to compute the matrix exponentials.

    Parameters
    ----------
    A : (N, N) array_like
        Input array.

    Returns
    -------
    coshm : (N, N) ndarray
        Hyperbolic matrix cosine of `A`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import tanhm, sinhm, coshm
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> c = coshm(a)
    >>> c
    array([[ 11.24592233,  38.76236492],
           [ 12.92078831,  50.00828725]])

    Verify tanhm(a) = sinhm(a).dot(inv(coshm(a)))

    >>> t = tanhm(a)
    >>> s = sinhm(a)
    >>> t - s.dot(np.linalg.inv(c))
    array([[  2.72004641e-15,   4.55191440e-15],
           [  0.00000000e+00,  -5.55111512e-16]])

    """
    A = _asarray_square(A)
    return _maybe_real(A, 0.5 * (expm(A) + expm(-A)))

