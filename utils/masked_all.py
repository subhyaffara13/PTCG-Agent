
def masked_all(shape, dtype=float):
    """
    Empty masked array with all elements masked.

    Return an empty masked array of the given shape and dtype, where all the
    data are masked.

    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the required MaskedArray, e.g., ``(2, 3)`` or ``2``.
    dtype : dtype, optional
        Data type of the output.

    Returns
    -------
    a : MaskedArray
        A masked array with all data masked.

    See Also
    --------
    masked_all_like : Empty masked array modelled on an existing array.

    Notes
    -----
    Unlike other masked array creation functions (e.g. `numpy.ma.zeros`,
    `numpy.ma.ones`, `numpy.ma.full`), `masked_all` does not initialize the
    values of the array, and may therefore be marginally faster. However,
    the values stored in the newly allocated array are arbitrary. For
    reproducible behavior, be sure to set each element of the array before
    reading.

    Examples
    --------
    >>> import numpy as np
    >>> np.ma.masked_all((3, 3))
    masked_array(
      data=[[--, --, --],
            [--, --, --],
            [--, --, --]],
      mask=[[ True,  True,  True],
            [ True,  True,  True],
            [ True,  True,  True]],
      fill_value=1e+20,
      dtype=float64)

    The `dtype` parameter defines the underlying data type.

    >>> a = np.ma.masked_all((3, 3))
    >>> a.dtype
    dtype('float64')
    >>> a = np.ma.masked_all((3, 3), dtype=np.int32)
    >>> a.dtype
    dtype('int32')

    """
    a = masked_array(np.empty(shape, dtype),
                     mask=np.ones(shape, make_mask_descr(dtype)))
    return a

