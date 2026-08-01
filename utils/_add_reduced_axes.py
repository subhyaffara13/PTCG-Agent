
def _add_reduced_axes(res, reduced_axes, keepdims, xp=np):
    """
    Add reduced axes back to all the arrays in the result object
    if keepdims = True.
    """
    return ([xpx.expand_dims(output, axis=reduced_axes)
             if not isinstance(output, int) else output for output in res]
            if keepdims else res)

