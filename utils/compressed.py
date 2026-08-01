
def compressed(x):
    """
    Return all the non-masked data as a 1-D array.

    This function is equivalent to calling the "compressed" method of a
    `ma.MaskedArray`, see `ma.MaskedArray.compressed` for details.

    See Also
    --------
    ma.MaskedArray.compressed : Equivalent method.

    Examples
    --------
    >>> import numpy as np

    Create an array with negative values masked:

    >>> import numpy as np
    >>> x = np.array([[1, -1, 0], [2, -1, 3], [7, 4, -1]])
    >>> masked_x = np.ma.masked_array(x, mask=x < 0)
    >>> masked_x
    masked_array(
      data=[[1, --, 0],
            [2, --, 3],
            [7, 4, --]],
      mask=[[False,  True, False],
            [False,  True, False],
            [False, False,  True]],
      fill_value=999999)

    Compress the masked array into a 1-D array of non-masked values:

    >>> np.ma.compressed(masked_x)
    array([1, 0, 2, 3, 7, 4])

    """
    return asanyarray(x).compressed()

