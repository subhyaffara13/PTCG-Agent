
def _get_funcs(
    names, arrays, dtype, lib_name, fmodule, fmodule_name, alias, ilp64="preferred"
):
    """
    Return available BLAS/LAPACK functions.

    Used also in lapack.py. See get_blas_funcs for docstring.
    """

    funcs = []
    unpack = False
    dtype = np.dtype(dtype)

    if isinstance(names, str):
        names = (names,)
        unpack = True

    prefix, dtype, _ = find_best_blas_type(arrays, dtype)

    for name in names:
        func_name = prefix + name
        func_name = alias.get(func_name, func_name)
        func = getattr(fmodule, func_name, None)
        if func is None:
            raise ValueError(
                f'{lib_name} function {func_name} could not be found')
        func.module_name, func.typecode, func.dtype = fmodule_name, prefix, dtype
        if not ilp64:
            func.int_dtype = np.dtype(np.intc)
        else:
            func.int_dtype = np.dtype(np.int64)
        func.prefix = prefix  # Backward compatibility
        funcs.append(func)

    if unpack:
        return funcs[0]
    else:
        return funcs

