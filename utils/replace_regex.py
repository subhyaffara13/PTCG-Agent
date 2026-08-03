import re

def replace_regex(
    values: ArrayLike, rx: re.Pattern, value, mask: npt.NDArray[np.bool_] | None
) -> None:
    """
    Parameters
    ----------
    values : ArrayLike
        Object dtype.
    rx : re.Pattern
    value : Any
    mask : np.ndarray[bool], optional

    Notes
    -----
    Alters values in-place.
    """

    # deal with replacing values with objects (strings) that match but
    # whose replacement is not a string (numeric, nan, object)
    if isna(value) or not isinstance(value, str):

        def re_replacer(s):
            if is_re(rx) and isinstance(s, str):
                return value if rx.search(s) is not None else s
            else:
                return s

    else:
        # value is guaranteed to be a string here, s can be either a string
        # or null if it's null it gets returned
        def re_replacer(s):
            if is_re(rx) and isinstance(s, str):
                return rx.sub(value, s)
            else:
                return s

    f = np.vectorize(re_replacer, otypes=[np.object_])

    if mask is None:
        values[:] = f(values)
    else:
        if values.ndim != mask.ndim:
            mask = np.broadcast_to(mask, values.shape)
        values[mask] = f(values[mask])

