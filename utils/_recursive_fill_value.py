
def _recursive_fill_value(dtype, f):
    """
    Recursively produce a fill value for `dtype`, calling f on scalar dtypes
    """
    if dtype.names is not None:
        # We wrap into `array` here, which ensures we use NumPy cast rules
        # for integer casts, this allows the use of 99999 as a fill value
        # for int8.
        vals = []
        for name in dtype.names:
            field_dtype = dtype[name]
            val = _recursive_fill_value(field_dtype, f)
            if np.issubdtype(field_dtype, np.datetime64):
                if isinstance(val, dt.date):
                    val = np.datetime64(val)
                    val = np.array(val)
                elif isinstance(val, (int, np.integer)):
                    val = np.array(val).astype(field_dtype)
                else:
                    val = np.array(val)
            else:
                val = np.array(val)
            vals.append(val)
        return np.array(tuple(vals), dtype=dtype)[()]  # decay to void scalar from 0d
    elif dtype.subdtype:
        subtype, shape = dtype.subdtype
        subval = _recursive_fill_value(subtype, f)
        return np.full(shape, subval)
    else:
        return f(dtype)

