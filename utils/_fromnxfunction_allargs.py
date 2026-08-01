
def _fromnxfunction_allargs(npfunc, /, *arys, **kwargs):
    """
    Wraps a NumPy function that can be called with multiple array arguments.
    All args are converted to arrays even if they are not so already.
    This makes it possible to process scalars as 1-D arrays.
    Only keyword arguments are passed through verbatim for the data and mask calls.
    Arrays arguments are processed independently and the results are returned in a list.
    If only one arg is present, the return value is just the processed array instead of
    a list.
    """
    out = tuple(
        masked_array(
            data=npfunc(np.asarray(a), **kwargs),
            mask=npfunc(getmaskarray(a), **kwargs),
        )
        for a in arys
    )
    return out[0] if len(out) == 1 else out

