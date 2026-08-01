
def order_filter(a, domain, rank):
    """
    Perform an order filter on an N-D array.

    Perform an order filter on the array in. The domain argument acts as a
    mask centered over each pixel. The non-zero elements of domain are
    used to select elements surrounding each input pixel which are placed
    in a list. The list is sorted, and the output for that pixel is the
    element corresponding to rank in the sorted list.

    Parameters
    ----------
    a : ndarray
        The N-dimensional input array.
    domain : array_like
        A mask array with the same number of dimensions as `a`.
        Each dimension should have an odd number of elements.
    rank : int
        A non-negative integer which selects the element from the
        sorted list (0 corresponds to the smallest element, 1 is the
        next smallest element, etc.).

    Returns
    -------
    out : ndarray
        The results of the order filter in an array with the same
        shape as `a`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> x = np.arange(25).reshape(5, 5)
    >>> domain = np.identity(3)
    >>> x
    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14],
           [15, 16, 17, 18, 19],
           [20, 21, 22, 23, 24]])
    >>> signal.order_filter(x, domain, 0)
    array([[  0,   0,   0,   0,   0],
           [  0,   0,   1,   2,   0],
           [  0,   5,   6,   7,   0],
           [  0,  10,  11,  12,   0],
           [  0,   0,   0,   0,   0]])
    >>> signal.order_filter(x, domain, 2)
    array([[  6,   7,   8,   9,   4],
           [ 11,  12,  13,  14,   9],
           [ 16,  17,  18,  19,  14],
           [ 21,  22,  23,  24,  19],
           [ 20,  21,  22,  23,  24]])

    """
    xp = array_namespace(a, domain)

    domain = xp.asarray(domain)
    for dimsize in domain.shape:
        if (dimsize % 2) != 1:
            raise ValueError("Each dimension of domain argument "
                             "should have an odd number of elements.")

    a = xp.asarray(a)
    if not (
        xp.isdtype(a.dtype, "integral") or a.dtype in (xp.float32, xp.float64)
    ):
        raise ValueError(f"dtype={a.dtype} is not supported by order_filter")
    result = ndimage.rank_filter(a, rank, footprint=domain, mode='constant')
    return result

