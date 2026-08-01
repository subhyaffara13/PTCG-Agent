
def fromflex(fxarray):
    """
    Build a masked array from a suitable flexible-type array.

    The input array has to have a data-type with ``_data`` and ``_mask``
    fields. This type of array is output by `MaskedArray.toflex`.

    Parameters
    ----------
    fxarray : ndarray
        The structured input array, containing ``_data`` and ``_mask``
        fields. If present, other fields are discarded.

    Returns
    -------
    result : MaskedArray
        The constructed masked array.

    See Also
    --------
    MaskedArray.toflex : Build a flexible-type array from a masked array.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array(np.arange(9).reshape(3, 3), mask=[0] + [1, 0] * 4)
    >>> rec = x.toflex()
    >>> rec
    array([[(0, False), (1,  True), (2, False)],
           [(3,  True), (4, False), (5,  True)],
           [(6, False), (7,  True), (8, False)]],
          dtype=[('_data', '<i8'), ('_mask', '?')])
    >>> x2 = np.ma.fromflex(rec)
    >>> x2
    masked_array(
      data=[[0, --, 2],
            [--, 4, --],
            [6, --, 8]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=999999)

    Extra fields can be present in the structured array but are discarded:

    >>> dt = [('_data', '<i4'), ('_mask', '|b1'), ('field3', '<f4')]
    >>> rec2 = np.zeros((2, 2), dtype=dt)
    >>> rec2
    array([[(0, False, 0.), (0, False, 0.)],
           [(0, False, 0.), (0, False, 0.)]],
          dtype=[('_data', '<i4'), ('_mask', '?'), ('field3', '<f4')])
    >>> y = np.ma.fromflex(rec2)
    >>> y
    masked_array(
      data=[[0, 0],
            [0, 0]],
      mask=[[False, False],
            [False, False]],
      fill_value=np.int64(999999),
      dtype=int32)

    """
    return masked_array(fxarray['_data'], mask=fxarray['_mask'])

