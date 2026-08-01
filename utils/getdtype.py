
def getdtype(dtype, a=None, default=None):
    """Form a supported numpy dtype based on input arguments.

    Returns a valid ``numpy.dtype`` from `dtype` if not None,
    or else ``a.dtype`` if possible, or else the given `default`
    if not None, or else raise a ``TypeError``.

    The resulting ``dtype`` must be in ``supported_dtypes``:
        bool_, int8, uint8, int16, uint16, int32, uint32,
        int64, uint64, longlong, ulonglong, float32, float64,
        longdouble, complex64, complex128, clongdouble
    """
    if dtype is None:
        try:
            newdtype = a.dtype
        except AttributeError as e:
            if default is not None:
                newdtype = np.dtype(default)
            else:
                raise TypeError("could not interpret data type") from e
    else:
        newdtype = np.dtype(dtype)

    if newdtype not in supported_dtypes:
        supported_dtypes_fmt = ", ".join(t.__name__ for t in supported_dtypes)
        raise ValueError(f"scipy.sparse does not support dtype {newdtype}. "
                         f"The only supported types are: {supported_dtypes_fmt}.")
    return newdtype

