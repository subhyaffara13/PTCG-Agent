
def _assign_where(out, result, where) -> None:
    """
    Set a ufunc result into 'out', masking with a 'where' argument if necessary.
    """
    if where is None:
        # no 'where' arg passed to ufunc
        out[:] = result
    else:
        np.putmask(out, where, result)

