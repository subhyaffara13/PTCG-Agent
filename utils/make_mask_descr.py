
def make_mask_descr(ndtype):
    """
    Construct a dtype description list from a given dtype.

    Returns a new dtype object, with the type of all fields in `ndtype` to a
    boolean type. Field names are not altered.

    Parameters
    ----------
    ndtype : dtype
        The dtype to convert.

    Returns
    -------
    result : dtype
        A dtype that looks like `ndtype`, the type of all fields is boolean.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> dtype = np.dtype({'names':['foo', 'bar'],
    ...                   'formats':[np.float32, np.int64]})
    >>> dtype
    dtype([('foo', '<f4'), ('bar', '<i8')])
    >>> ma.make_mask_descr(dtype)
    dtype([('foo', '|b1'), ('bar', '|b1')])
    >>> ma.make_mask_descr(np.float32)
    dtype('bool')

    """
    return _replace_dtype_fields(ndtype, MaskType)

