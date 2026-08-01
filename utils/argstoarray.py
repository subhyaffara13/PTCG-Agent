
def argstoarray(*args):
    """
    Constructs a 2D array from a group of sequences.

    Sequences are filled with missing values to match the length of the longest
    sequence.

    Parameters
    ----------
    *args : sequences
        Group of sequences.

    Returns
    -------
    argstoarray : MaskedArray
        A ( `m` x `n` ) masked array, where `m` is the number of arguments and
        `n` the length of the longest argument.

    Notes
    -----
    `numpy.ma.vstack` has identical behavior, but is called with a sequence
    of sequences.

    Examples
    --------
    A 2D masked array constructed from a group of sequences is returned.

    >>> from scipy.stats.mstats import argstoarray
    >>> argstoarray([1, 2, 3], [4, 5, 6])
    masked_array(
     data=[[1.0, 2.0, 3.0],
           [4.0, 5.0, 6.0]],
     mask=[[False, False, False],
           [False, False, False]],
     fill_value=1e+20)

    The returned masked array filled with missing values when the lengths of
    sequences are different.

    >>> argstoarray([1, 3], [4, 5, 6])
    masked_array(
     data=[[1.0, 3.0, --],
           [4.0, 5.0, 6.0]],
     mask=[[False, False,  True],
           [False, False, False]],
     fill_value=1e+20)

    """
    if len(args) == 1 and not isinstance(args[0], ndarray):
        output = ma.asarray(args[0])
        if output.ndim != 2:
            raise ValueError("The input should be 2D")
    else:
        n = len(args)
        m = max([len(k) for k in args])
        output = ma.array(np.empty((n,m), dtype=float), mask=True)
        for (k,v) in enumerate(args):
            output[k,:len(v)] = v

    output[np.logical_not(np.isfinite(output._data))] = masked
    return output

