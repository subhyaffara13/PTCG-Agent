
def _lazy_valid_checks(*args, throw=False, warning=False, materialize=False, xp):
    """Validate a set of conditions on the contents of possibly lazy arrays.

    Parameters
    ----------
    args : tuples of (Array, str)
        The first element of each tuple must be a 0-dimensional Array
        that evaluates to bool; the second element must be the message to convey
        if the  first element evaluates to True.
    throw: bool
        Set to True to `raise ValueError(args[i][1])` if `args[i][0]` is True.
    warning: bool
        Set to True to issue a warning with message `args[i][1]` if `args[i][0]`
        is True.
    materialize: bool
        Set to True to force materialization of lazy arrays when throw=True or
        warning=True. If the inputs are lazy and materialize=False, ignore the
        `throw` and `warning` flags.
    xp: module
        Array API namespace

    Returns
    -------
    If xp is an eager backend (e.g. numpy) and all conditions are False, return True.
    If throw is True, raise. Otherwise, return False.

    If xp is a lazy backend (e.g. Dask or JAX), return a 0-dimensional bool Array.
    """
    conds = xp.concat([xp.reshape(cond, (1, )) for cond, _ in args])

    lazy = is_lazy_array(conds)
    if not throw and not warning or (lazy and not materialize):
        out = ~xp.any(conds)
        return out if lazy else bool(out)

    if is_dask(xp):
        # Only materialize the graph once, instead of once per check
        conds = conds.compute()

    # Don't call np.asarray(conds), as it would be blocked by the device transfer
    # guard on CuPy and PyTorch and the densification guard on Sparse, whereas
    # bool() will not.
    conds = [bool(cond) for cond in conds]

    for cond, (_, msg) in zip(conds, args):
        if throw and cond:
            raise ValueError(msg)
        elif warning and cond:
            warnings.warn(msg, ClusterWarning, stacklevel=3)

    return not any(conds)

