
def _check_mask_axis(mask, axis, keepdims=np._NoValue):
    "Check whether there are masked values along the given axis"
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    if mask is not nomask:
        return mask.all(axis=axis, **kwargs)
    return nomask

