import functools

def _add_keepdims(func):
    """ hack in keepdims behavior into a function taking an axis """
    @functools.wraps(func)
    def wrapped(a, axis, **kwargs):
        res = func(a, axis=axis, **kwargs)
        if axis is None:
            axis = 0  # res is now a scalar, so we can insert this anywhere
        return np.expand_dims(res, axis=axis)
    return wrapped

