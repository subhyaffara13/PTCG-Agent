
def _check_fill_value(fill_value, ndtype):
    """
    Private function validating the given `fill_value` for the given dtype.

    If fill_value is None, it is set to the default corresponding to the dtype.

    If fill_value is not None, its value is forced to the given dtype.

    The result is always a 0d array.

    """
    ndtype = np.dtype(ndtype)
    if fill_value is None:
        fill_value = default_fill_value(ndtype)
        # TODO: It seems better to always store a valid fill_value, the oddity
        #       about is that `_fill_value = None` would behave even more
        #       different then.
        #       (e.g. this allows arr_uint8.astype(int64) to have the default
        #       fill value again...)
        # The one thing that changed in 2.0/2.1 around cast safety is that the
        # default `int(99...)` is not a same-kind cast anymore, so if we
        # have a uint, use the default uint.
        if ndtype.kind == "u":
            fill_value = np.uint(fill_value)
    elif ndtype.names is not None:
        if isinstance(fill_value, (ndarray, np.void)):
            try:
                fill_value = np.asarray(fill_value, dtype=ndtype)
            except ValueError as e:
                err_msg = "Unable to transform %s to dtype %s"
                raise ValueError(err_msg % (fill_value, ndtype)) from e
        else:
            fill_value = np.asarray(fill_value, dtype=object)
            fill_value = np.array(_recursive_set_fill_value(fill_value, ndtype),
                                  dtype=ndtype)
    elif isinstance(fill_value, str) and (ndtype.char not in 'OSTVU'):
        # Note this check doesn't work if fill_value is not a scalar
        err_msg = "Cannot set fill value of string with array of dtype %s"
        raise TypeError(err_msg % ndtype)
    else:
        # In case we want to convert 1e20 to int.
        # Also in case of converting string arrays.
        try:
            fill_value = np.asarray(fill_value, dtype=ndtype)
        except (OverflowError, ValueError) as e:
            # Raise TypeError instead of OverflowError or ValueError.
            # OverflowError is seldom used, and the real problem here is
            # that the passed fill_value is not compatible with the ndtype.
            err_msg = "Cannot convert fill_value %s to dtype %s"
            raise TypeError(err_msg % (fill_value, ndtype)) from e
    return np.array(fill_value)

