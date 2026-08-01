
def _has_bool_dtype(x):
    try:
        return x.dtype == bool
    except AttributeError:
        return isinstance(x, (bool, np.bool_))

