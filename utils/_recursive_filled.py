
def _recursive_filled(a, mask, fill_value):
    """
    Recursively fill `a` with `fill_value`.

    """
    names = a.dtype.names
    for name in names:
        current = a[name]
        if current.dtype.names is not None:
            _recursive_filled(current, mask[name], fill_value[name])
        else:
            np.copyto(current, fill_value[name], where=mask[name])

