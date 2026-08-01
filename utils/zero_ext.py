
def zero_ext(x, n, axis=-1):
    """
    Zero padding at the boundaries of an array

    Generate a new ndarray that is a zero-padded extension of `x` along
    an axis.

    Parameters
    ----------
    x : ndarray
        The array to be extended.
    n : int
        The number of elements by which to extend `x` at each end of the
        axis.
    axis : int, optional
        The axis along which to extend `x`. Default is -1.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.signal._arraytools import zero_ext
    >>> a = np.array([[1, 2, 3, 4, 5], [0, 1, 4, 9, 16]])
    >>> zero_ext(a, 2)
    array([[ 0,  0,  1,  2,  3,  4,  5,  0,  0],
           [ 0,  0,  0,  1,  4,  9, 16,  0,  0]])
    """
    if n < 1:
        return x
    zeros_shape = list(x.shape)
    zeros_shape[axis] = n
    zeros = np.zeros(zeros_shape, dtype=x.dtype)
    ext = np.concatenate((zeros, x, zeros), axis=axis)
    return ext

