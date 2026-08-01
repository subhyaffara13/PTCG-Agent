
def _fromnxfunction_single(npfunc, a, /, *args, **kwargs):
    """
    Wraps a NumPy function that can be called with a single array argument followed by
    auxiliary args that are passed verbatim for both the data and mask calls.
    """
    return masked_array(
        data=npfunc(np.asarray(a), *args, **kwargs),
        mask=npfunc(getmaskarray(a), *args, **kwargs),
    )

