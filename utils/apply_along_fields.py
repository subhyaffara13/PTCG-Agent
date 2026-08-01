
def apply_along_fields(func, arr):
    """
    Apply function 'func' as a reduction across fields of a structured array.

    This is similar to `numpy.apply_along_axis`, but treats the fields of a
    structured array as an extra axis. The fields are all first cast to a
    common type following the type-promotion rules from `numpy.result_type`
    applied to the field's dtypes.

    Parameters
    ----------
    func : function
       Function to apply on the "field" dimension. This function must
       support an `axis` argument, like `numpy.mean`, `numpy.sum`, etc.
    arr : ndarray
       Structured array for which to apply func.

    Returns
    -------
    out : ndarray
       Result of the reduction operation

    Examples
    --------
    >>> import numpy as np

    >>> from numpy.lib import recfunctions as rfn
    >>> b = np.array([(1, 2, 5), (4, 5, 7), (7, 8 ,11), (10, 11, 12)],
    ...              dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    >>> rfn.apply_along_fields(np.mean, b)
    array([ 2.66666667,  5.33333333,  8.66666667, 11.        ])
    >>> rfn.apply_along_fields(np.mean, b[['x', 'z']])
    array([ 3. ,  5.5,  9. , 11. ])

    """
    if arr.dtype.names is None:
        raise ValueError('arr must be a structured array')

    uarr = structured_to_unstructured(arr)
    return func(uarr, axis=-1)

