
def compress_nd(x, axis=None):
    """Suppress slices from multiple dimensions which contain masked values.

    Parameters
    ----------
    x : array_like, MaskedArray
        The array to operate on. If not a MaskedArray instance (or if no array
        elements are masked), `x` is interpreted as a MaskedArray with `mask`
        set to `nomask`.
    axis : tuple of ints or int, optional
        Which dimensions to suppress slices from can be configured with this
        parameter.
        - If axis is a tuple of ints, those are the axes to suppress slices from.
        - If axis is an int, then that is the only axis to suppress slices from.
        - If axis is None, all axis are selected.

    Returns
    -------
    compress_array : ndarray
        The compressed array.

    Examples
    --------
    >>> import numpy as np
    >>> arr = [[1, 2], [3, 4]]
    >>> mask = [[0, 1], [0, 0]]
    >>> x = np.ma.array(arr, mask=mask)
    >>> np.ma.compress_nd(x, axis=0)
    array([[3, 4]])
    >>> np.ma.compress_nd(x, axis=1)
    array([[1],
           [3]])
    >>> np.ma.compress_nd(x)
    array([[3]])

    """
    x = asarray(x)
    m = getmask(x)
    # Set axis to tuple of ints
    if axis is None:
        axis = tuple(range(x.ndim))
    else:
        axis = normalize_axis_tuple(axis, x.ndim)

    # Nothing is masked: return x
    if m is nomask or not m.any():
        return x._data
    # All is masked: return empty
    if m.all():
        return nxarray([])
    # Filter elements through boolean indexing
    data = x._data
    for ax in axis:
        axes = tuple(list(range(ax)) + list(range(ax + 1, x.ndim)))
        data = data[(slice(None),) * ax + (~m.any(axis=axes),)]
    return data

