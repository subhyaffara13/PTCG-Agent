
def eager_shape(x: Array, /, axis: int | None = None) -> tuple[int, ...]:
    """
    Return shape of an array. Raise if shape is not fully defined.

    Parameters
    ----------
    x : Array
        Input array.
    axis : int, optional
        If provided, only returns the tuple (shape[axis],).

    Returns
    -------
    tuple[int, ...]
        Shape of the array.
    """
    shape = x.shape
    if axis is not None:
        s = shape[axis]
        # Dask arrays uses non-standard NaN instead of None
        if s is None or math.isnan(s):
            msg = f"Unsupported lazy shape for axis {axis}"
            raise TypeError(msg)
        return (s,)

    if any(s is None or math.isnan(s) for s in shape):
        msg = "Unsupported lazy shape"
        raise TypeError(msg)
    return cast(tuple[int, ...], shape)

