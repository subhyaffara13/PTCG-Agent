
def nunique(x: Array, /, *, xp: ModuleType | None = None) -> Array:
    """
    Count the number of unique elements in an array.

    Compatible with JAX and Dask, whose laziness would be otherwise
    problematic.

    Parameters
    ----------
    x : Array
        Input array.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array: 0-dimensional integer array
        The number of unique elements in `x`. It can be lazy.
    """
    if xp is None:
        xp = array_namespace(x)

    if is_jax_array(x):
        # size= is JAX-specific
        # https://github.com/data-apis/array-api/issues/883
        _, counts = xp.unique_counts(x, size=_compat.size(x))
        return (counts > 0).sum()

    # There are 3 general use cases:
    # 1. backend has unique_counts and it returns an array with known shape
    # 2. backend has unique_counts and it returns a None-sized array;
    #    e.g. Dask, ndonnx
    # 3. backend does not have unique_counts; e.g. wrapped JAX
    if capabilities(xp, device=_compat.device(x))["data-dependent shapes"]:
        # xp has unique_counts; O(n) complexity
        _, counts = xp.unique_counts(x)
        n = _compat.size(counts)
        if n is None:
            return xp.sum(xp.ones_like(counts))
        return xp.asarray(n, device=_compat.device(x))

    # xp does not have unique_counts; O(n*logn) complexity
    x = xp.reshape(x, (-1,))
    x = xp.sort(x, stable=False)
    mask = x != xp.roll(x, -1)
    default_int = default_dtype(xp, "integral", device=_compat.device(x))
    return xp.maximum(
        # Special cases:
        # - array is size 0
        # - array has all elements equal to each other
        xp.astype(xp.any(~mask), default_int),
        xp.sum(xp.astype(mask, default_int)),
    )

