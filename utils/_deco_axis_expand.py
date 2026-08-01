
def _deco_axis_expand(func):
    """
    Generically handle axis arguments in reductions.
    axis is *always* the 2nd arg in the function so no need to have a look at its signature
    """

    @functools.wraps(func)
    def wrapped(a, axis=None, *args, **kwds):
        if axis is not None:
            axis = _util.normalize_axis_tuple(axis, a.ndim)

        if axis == ():
            # So we insert a length-one axis and run the reduction along it.
            # We cannot return a.clone() as this would sidestep the checks inside the function
            newshape = _util.expand_shape(a.shape, axis=0)
            a = a.reshape(newshape)
            axis = (0,)

        return func(a, axis, *args, **kwds)

    return wrapped

