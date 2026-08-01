
def _compatible_boolean_index(idx, desired_ndim):
    """Check for boolean array or array-like. peek before asarray for array-like"""
    # use attribute ndim to indicate a compatible array and check dtype
    # if not, look at 1st element as quick rejection of bool, else slower asanyarray
    if not hasattr(idx, 'ndim'):
        # is first element boolean?
        try:
            ix = next(iter(idx), None)
            for _ in range(desired_ndim):
                if isinstance(ix, bool):
                    break
                ix = next(iter(ix), None)
            else:
                return None
        except TypeError:
            return None
        # since first is boolean, construct array and check all elements
        idx = np.asanyarray(idx)

    if idx.dtype.kind == 'b':
        return idx
    return None

