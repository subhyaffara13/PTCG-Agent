
def _memoize_get_funcs(func):
    """
    Memoized fast path for _get_funcs instances
    """
    memo = {}
    func.memo = memo

    @functools.wraps(func)
    def getter(names, arrays=(), dtype=None, ilp64="preferred"):
        key = (names, dtype, ilp64)
        for array in arrays:
            # cf. find_blas_funcs
            key += (array.dtype.char, array.flags.fortran)

        try:
            value = memo.get(key)
        except TypeError:
            # unhashable key etc.
            key = None
            value = None

        if value is not None:
            return value

        value = func(names, arrays, dtype, ilp64)

        if key is not None:
            memo[key] = value

        return value

    return getter

