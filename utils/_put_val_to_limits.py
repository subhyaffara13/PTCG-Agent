
def _put_val_to_limits(a, limits, inclusive, val=np.nan, xp=None):
    """Replace elements outside limits with a value.

    This is primarily a utility function.

    Parameters
    ----------
    a : array
    limits : (float or None, float or None)
        A tuple consisting of the (lower limit, upper limit).  Elements in the
        input array less than the lower limit or greater than the upper limit
        will be replaced with `val`. None implies no limit.
    inclusive : (bool, bool)
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to lower or upper are allowed.
    val : float, default: NaN
        The value with which extreme elements of the array are replaced.

    """
    xp = array_namespace(a) if xp is None else xp
    mask = xp.zeros_like(a, dtype=xp.bool)
    if limits is None:
        return a, mask
    lower_limit, upper_limit = limits
    lower_include, upper_include = inclusive
    if lower_limit is not None:
        mask = mask | ((a < lower_limit) if lower_include else a <= lower_limit)
    if upper_limit is not None:
        mask = mask | ((a > upper_limit) if upper_include else a >= upper_limit)
    lazy = is_lazy_array(mask)
    if not lazy and xp.all(mask):
        raise ValueError("No array values within given limits")
    if lazy or xp.any(mask):
        a = xp.where(mask, val, a)
    return a, mask

