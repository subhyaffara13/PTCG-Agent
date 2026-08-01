
def _normalize_lapack_dtype(a, overwrite_a):
    """Make sure an input array has a LAPACK-compatible dtype, cast and copy otherwise.
    """
    _, dtyp, _ = find_best_lapack_type((a,))
    needs_copy = dtyp.char != a.dtype.char  # .char to tell 'g' from 'd' on arm
    if needs_copy:
        a = a.astype(dtyp)   # makes a copy, free to scratch
    return a, overwrite_a or needs_copy

