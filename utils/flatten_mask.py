
def flatten_mask(mask):
    """
    Returns a completely flattened version of the mask, where nested fields
    are collapsed.

    Parameters
    ----------
    mask : array_like
        Input array, which will be interpreted as booleans.

    Returns
    -------
    flattened_mask : ndarray of bools
        The flattened input.

    Examples
    --------
    >>> import numpy as np
    >>> mask = np.array([0, 0, 1])
    >>> np.ma.flatten_mask(mask)
    array([False, False,  True])

    >>> mask = np.array([(0, 0), (0, 1)], dtype=[('a', bool), ('b', bool)])
    >>> np.ma.flatten_mask(mask)
    array([False, False, False,  True])

    >>> mdtype = [('a', bool), ('b', [('ba', bool), ('bb', bool)])]
    >>> mask = np.array([(0, (0, 0)), (0, (0, 1))], dtype=mdtype)
    >>> np.ma.flatten_mask(mask)
    array([False, False, False, False, False,  True])

    """

    def _flatmask(mask):
        "Flatten the mask and returns a (maybe nested) sequence of booleans."
        mnames = mask.dtype.names
        if mnames is not None:
            return [flatten_mask(mask[name]) for name in mnames]
        else:
            return mask

    def _flatsequence(sequence):
        "Generates a flattened version of the sequence."
        try:
            for element in sequence:
                if hasattr(element, '__iter__'):
                    yield from _flatsequence(element)
                else:
                    yield element
        except TypeError:
            yield sequence

    mask = np.asarray(mask)
    flattened = _flatsequence(_flatmask(mask))
    return np.array(list(flattened), dtype=bool)

