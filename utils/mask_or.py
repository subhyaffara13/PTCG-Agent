import copy

def mask_or(m1, m2, copy=False, shrink=True):
    """
    Combine two masks with the ``logical_or`` operator.

    The result may be a view on `m1` or `m2` if the other is `nomask`
    (i.e. False).

    Parameters
    ----------
    m1, m2 : array_like
        Input masks.
    copy : bool, optional
        If copy is False and one of the inputs is `nomask`, return a view
        of the other input mask. Defaults to False.
    shrink : bool, optional
        Whether to shrink the output to `nomask` if all its values are
        False. Defaults to True.

    Returns
    -------
    mask : output mask
        The result masks values that are masked in either `m1` or `m2`.

    Raises
    ------
    ValueError
        If `m1` and `m2` have different flexible dtypes.

    Examples
    --------
    >>> import numpy as np
    >>> m1 = np.ma.make_mask([0, 1, 1, 0])
    >>> m2 = np.ma.make_mask([1, 0, 0, 0])
    >>> np.ma.mask_or(m1, m2)
    array([ True,  True,  True, False])

    """

    if (m1 is nomask) or (m1 is False):
        dtype = getattr(m2, 'dtype', MaskType)
        return make_mask(m2, copy=copy, shrink=shrink, dtype=dtype)
    if (m2 is nomask) or (m2 is False):
        dtype = getattr(m1, 'dtype', MaskType)
        return make_mask(m1, copy=copy, shrink=shrink, dtype=dtype)
    if m1 is m2 and is_mask(m1):
        return _shrink_mask(m1) if shrink else m1
    (dtype1, dtype2) = (getattr(m1, 'dtype', None), getattr(m2, 'dtype', None))
    if dtype1 != dtype2:
        raise ValueError(f"Incompatible dtypes '{dtype1}'<>'{dtype2}'")
    if dtype1.names is not None:
        # Allocate an output mask array with the properly broadcast shape.
        newmask = np.empty(np.broadcast(m1, m2).shape, dtype1)
        _recursive_mask_or(m1, m2, newmask)
        return newmask
    return make_mask(umath.logical_or(m1, m2), copy=copy, shrink=shrink)

