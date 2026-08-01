
def _fromnxfunction_seq(npfunc, arys, /, *args, **kwargs):
    """
    Wraps a NumPy function that can be called with a single sequence of arrays followed
    by auxiliary args that are passed verbatim for both the data and mask calls.
    """
    return masked_array(
        data=npfunc(tuple(np.asarray(a) for a in arys), *args, **kwargs),
        mask=npfunc(tuple(getmaskarray(a) for a in arys), *args, **kwargs),
    )

