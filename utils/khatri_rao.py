
def khatri_rao(a, b):
    r"""
    Khatri-Rao product of two matrices.

    A column-wise Kronecker product of two matrices

    Parameters
    ----------
    a : (n, k) array_like
        Input array
    b : (m, k) array_like
        Input array

    Returns
    -------
    c:  (n*m, k) ndarray
        Khatri-rao product of `a` and `b`.

    Notes
    -----
    The mathematical definition of the Khatri-Rao product is:

    .. math::

        (A_{ij}  \bigotimes B_{ij})_{ij}

    which is the Kronecker product of every column of A and B, e.g.::

        c = np.vstack([np.kron(a[:, k], b[:, k]) for k in range(b.shape[1])]).T

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[1, 2, 3], [4, 5, 6]])
    >>> b = np.array([[3, 4, 5], [6, 7, 8], [2, 3, 9]])
    >>> linalg.khatri_rao(a, b)
    array([[ 3,  8, 15],
           [ 6, 14, 24],
           [ 2,  6, 27],
           [12, 20, 30],
           [24, 35, 48],
           [ 8, 15, 54]])

    """
    a = np.asarray(a)
    b = np.asarray(b)

    if not (a.ndim == 2 and b.ndim == 2):
        raise ValueError("The both arrays should be 2-dimensional.")

    if not a.shape[1] == b.shape[1]:
        raise ValueError("The number of columns for both arrays "
                         "should be equal.")

    # accommodate empty arrays
    if a.size == 0 or b.size == 0:
        m = a.shape[0] * b.shape[0]
        n = a.shape[1]
        return np.empty_like(a, shape=(m, n))

    # c = np.vstack([np.kron(a[:, k], b[:, k]) for k in range(b.shape[1])]).T
    c = a[..., :, np.newaxis, :] * b[..., np.newaxis, :, :]
    return c.reshape((-1,) + c.shape[2:])

