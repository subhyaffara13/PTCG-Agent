
def asanyarray(a, dtype=None, order=None):
    """
    Convert the input to a masked array, conserving subclasses.

    If `a` is a subclass of `MaskedArray`, its class is conserved.
    No copy is performed if the input is already an `ndarray`.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.
    dtype : dtype, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Memory layout.  'A' and 'K' depend on the order of input array ``a``.
        'C' row-major (C-style),
        'F' column-major (Fortran-style) memory representation.
        'A' (any) means 'F' if ``a`` is Fortran contiguous, 'C' otherwise
        'K' (keep) preserve input order
        Defaults to 'K'.

    Returns
    -------
    out : MaskedArray
        MaskedArray interpretation of `a`.

    See Also
    --------
    asarray : Similar to `asanyarray`, but does not conserve subclass.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(10.).reshape(2, 5)
    >>> x
    array([[0., 1., 2., 3., 4.],
           [5., 6., 7., 8., 9.]])
    >>> np.ma.asanyarray(x)
    masked_array(
      data=[[0., 1., 2., 3., 4.],
            [5., 6., 7., 8., 9.]],
      mask=False,
      fill_value=1e+20)
    >>> type(np.ma.asanyarray(x))
    <class 'numpy.ma.MaskedArray'>

    """
    # workaround for #8666, to preserve identity. Ideally the bottom line
    # would handle this for us.
    if (
        isinstance(a, MaskedArray)
        and (dtype is None or dtype == a.dtype)
        and (
            order in {None, 'A', 'K'}
            or order == 'C' and a.flags.carray
            or order == 'F' and a.flags.f_contiguous
        )
    ):
        return a
    return masked_array(a, dtype=dtype, copy=False, keep_mask=True, subok=True,
                        order=order)

