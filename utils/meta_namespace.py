
def meta_namespace(
    *arrays: Array | complex | None, xp: ModuleType | None = None
) -> ModuleType:
    """
    Get the namespace of Dask chunks.

    On all other backends, just return the namespace of the arrays.

    Parameters
    ----------
    *arrays : Array | int | float | complex | bool | None
        Input arrays.
    xp : array_namespace, optional
        The standard-compatible namespace for the input arrays. Default: infer.

    Returns
    -------
    array_namespace
        If xp is Dask, the namespace of the Dask chunks;
        otherwise, the namespace of the arrays.
    """
    xp = array_namespace(*arrays) if xp is None else xp
    if not is_dask_namespace(xp):
        return xp
    # Quietly skip scalars and None's
    metas = [cast(Array | None, getattr(a, "_meta", None)) for a in arrays]
    return array_namespace(*metas)

