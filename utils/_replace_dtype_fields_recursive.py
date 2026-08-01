
def _replace_dtype_fields_recursive(dtype, primitive_dtype):
    "Private function allowing recursion in _replace_dtype_fields."
    _recurse = _replace_dtype_fields_recursive

    # Do we have some name fields ?
    if dtype.names is not None:
        descr = []
        for name in dtype.names:
            field = dtype.fields[name]
            if len(field) == 3:
                # Prepend the title to the name
                name = (field[-1], name)
            descr.append((name, _recurse(field[0], primitive_dtype)))
        new_dtype = np.dtype(descr)

    # Is this some kind of composite a la (float,2)
    elif dtype.subdtype:
        descr = list(dtype.subdtype)
        descr[0] = _recurse(dtype.subdtype[0], primitive_dtype)
        new_dtype = np.dtype(tuple(descr))

    # this is a primitive type, so do a direct replacement
    else:
        new_dtype = primitive_dtype

    # preserve identity of dtypes
    if new_dtype == dtype:
        new_dtype = dtype

    return new_dtype

