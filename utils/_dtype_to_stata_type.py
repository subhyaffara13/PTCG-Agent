
def _dtype_to_stata_type(dtype: np.dtype, column: Series) -> int:
    """
    Convert dtype types to stata types. Returns the byte of the given ordinal.
    See TYPE_MAP and comments for an explanation. This is also explained in
    the dta spec.
    1 - 244 are strings of this length
                         Pandas    Stata
    251 - for int8      byte
    252 - for int16     int
    253 - for int32     long
    254 - for float32   float
    255 - for double    double

    If there are dates to convert, then dtype will already have the correct
    type inserted.
    """
    # TODO: expand to handle datetime to integer conversion
    if dtype.type is np.object_:  # try to coerce it to the biggest string
        # not memory efficient, what else could we
        # do?
        itemsize = max_len_string_array(ensure_object(column._values))
        return max(itemsize, 1)
    elif dtype.type is np.float64:
        return 255
    elif dtype.type is np.float32:
        return 254
    elif dtype.type is np.int32:
        return 253
    elif dtype.type is np.int16:
        return 252
    elif dtype.type is np.int8:
        return 251
    else:  # pragma : no cover
        raise NotImplementedError(f"Data type {dtype} not supported.")

