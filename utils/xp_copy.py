
def xp_copy(x: Array, *, xp: ModuleType | None = None) -> Array:
    """
    Copies an array.

    Parameters
    ----------
    x : array

    xp : array_namespace

    Returns
    -------
    copy : array
        Copied array

    Notes
    -----
    This copy function does not offer all the semantics of `np.copy`, i.e. the
    `subok` and `order` keywords are not used.
    """
    # Note: for older NumPy versions, `np.asarray` did not support the `copy` kwarg,
    # so this uses our other helper `_asarray`.
    if xp is None:
        xp = array_namespace(x)

    return _asarray(x, copy=True, xp=xp)

