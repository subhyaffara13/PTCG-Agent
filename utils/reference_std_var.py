
def reference_std_var(f):
    """Forwards unbiased/correction kwargs as NumPy's equivalent ddof"""
    g = reference_reduction_numpy(f)

    @wraps(g)
    def wrapper(x: npt.NDArray, *args, **kwargs):
        if 'unbiased' in kwargs and 'correction' in kwargs:
            raise AssertionError("Cannot specify both 'unbiased' and 'correction' in kwargs")

        if 'unbiased' in kwargs:
            kwargs['ddof'] = int(kwargs.pop('unbiased'))
        elif 'correction' in kwargs:
            kwargs['ddof'] = kwargs.pop('correction')

        return g(x, *args, **kwargs)

    return wrapper

