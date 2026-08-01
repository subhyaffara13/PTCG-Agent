
def _wrapreduction_any_all(obj, ufunc, method, axis, out, **kwargs):
    # Same as above function, but dtype is always bool (but never passed on)
    passkwargs = {k: v for k, v in kwargs.items()
                  if v is not np._NoValue}

    if type(obj) is not mu.ndarray:
        try:
            reduction = getattr(obj, method)
        except AttributeError:
            pass
        else:
            return reduction(axis=axis, out=out, **passkwargs)

    return ufunc.reduce(obj, axis, bool, out, **passkwargs)

