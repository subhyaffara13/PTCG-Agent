
def mask_rows(a, axis=np._NoValue):
    """
    Mask rows of a 2D array that contain masked values.

    This function is a shortcut to ``mask_rowcols`` with `axis` equal to 0.

    See Also
    --------
    mask_rowcols : Mask rows and/or columns of a 2D array.
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.zeros((3, 3), dtype=np.int_)
    >>> a[1, 1] = 1
    >>> a
    array([[0, 0, 0],
           [0, 1, 0],
           [0, 0, 0]])
    >>> a = np.ma.masked_equal(a, 1)
    >>> a
    masked_array(
      data=[[0, 0, 0],
            [0, --, 0],
            [0, 0, 0]],
      mask=[[False, False, False],
            [False,  True, False],
            [False, False, False]],
      fill_value=1)

    >>> np.ma.mask_rows(a)
    masked_array(
      data=[[0, 0, 0],
            [--, --, --],
            [0, 0, 0]],
      mask=[[False, False, False],
            [ True,  True,  True],
            [False, False, False]],
      fill_value=1)

    """
    if axis is not np._NoValue:
        # remove the axis argument when this deprecation expires
        # NumPy 1.18.0, 2019-11-28
        warnings.warn(
            "The axis argument has always been ignored, in future passing it "
            "will raise TypeError", DeprecationWarning, stacklevel=2)
    return mask_rowcols(a, 0)

