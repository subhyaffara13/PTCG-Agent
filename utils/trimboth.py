
def trimboth(data, proportiontocut=0.2, inclusive=(True,True), axis=None):
    """
    Trims the smallest and largest data values.

    Trims the `data` by masking the ``int(proportiontocut * n)`` smallest and
    ``int(proportiontocut * n)`` largest values of data along the given axis,
    where n is the number of unmasked values before trimming.

    Parameters
    ----------
    data : ndarray
        Data to trim.
    proportiontocut : float, optional
        Percentage of trimming (as a float between 0 and 1).
        If n is the number of unmasked values before trimming, the number of
        values after trimming is ``(1 - 2*proportiontocut) * n``.
        Default is 0.2.
    inclusive : {(bool, bool) tuple}, optional
        Tuple indicating whether the number of data being masked on each side
        should be rounded (True) or truncated (False).
    axis : int, optional
        Axis along which to perform the trimming.
        If None, the input array is first flattened.

    """  # numpydoc ignore=RT01
    return trimr(data, limits=(proportiontocut,proportiontocut),
                 inclusive=inclusive, axis=axis)


def trimboth(a, proportiontocut, axis=0):
    """Slice off a proportion of items from both ends of an array.

    Slice off the passed proportion of items from both ends of the passed
    array (i.e., with `proportiontocut` = 0.1, slices leftmost 10% **and**
    rightmost 10% of scores). The trimmed values are the lowest and
    highest ones.
    Slice off less if proportion results in a non-integer slice index (i.e.
    conservatively slices off `proportiontocut`).

    Parameters
    ----------
    a : array_like
        Data to trim.
    proportiontocut : float
        Proportion (in range 0-1) of total data set to trim of each end.
    axis : int or None, optional
        Axis along which to trim data. Default is 0. If None, compute over
        the whole array `a`.

    Returns
    -------
    out : ndarray
        Trimmed version of array `a`. The order of the trimmed content
        is undefined.

    See Also
    --------
    trim_mean

    Examples
    --------
    Create an array of 10 values and trim 10% of those values from each end:

    >>> import numpy as np
    >>> from scipy import stats
    >>> a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> stats.trimboth(a, 0.1)
    array([1, 3, 2, 4, 5, 6, 7, 8])

    Note that the elements of the input array are trimmed by value, but the
    output array is not necessarily sorted.

    The proportion to trim is rounded down to the nearest integer. For
    instance, trimming 25% of the values from each end of an array of 10
    values will return an array of 6 values:

    >>> b = np.arange(10)
    >>> stats.trimboth(b, 1/4).shape
    (6,)

    Multidimensional arrays can be trimmed along any axis or across the entire
    array:

    >>> c = [2, 4, 6, 8, 0, 1, 3, 5, 7, 9]
    >>> d = np.array([a, b, c])
    >>> stats.trimboth(d, 0.4, axis=0).shape
    (1, 10)
    >>> stats.trimboth(d, 0.4, axis=1).shape
    (3, 2)
    >>> stats.trimboth(d, 0.4, axis=None).shape
    (6,)

    """
    a = np.asarray(a)

    if a.size == 0:
        return a

    if axis is None:
        a = a.ravel()
        axis = 0

    nobs = a.shape[axis]
    lowercut = int(proportiontocut * nobs)
    uppercut = nobs - lowercut
    if (lowercut >= uppercut):
        raise ValueError("Proportion too big.")

    atmp = np.partition(a, (lowercut, uppercut - 1), axis)

    sl = [slice(None)] * atmp.ndim
    sl[axis] = slice(lowercut, uppercut)
    return atmp[tuple(sl)]

