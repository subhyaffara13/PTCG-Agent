
def _mask_propagate(a, axis):
    """
    Mask whole 1-d vectors of an array that contain masked values.
    """
    a = array(a, subok=False)
    m = getmask(a)
    if m is nomask or not m.any() or axis is None:
        return a
    a._mask = a._mask.copy()
    axes = normalize_axis_tuple(axis, a.ndim)
    for ax in axes:
        a._mask |= m.any(axis=ax, keepdims=True)
    return a

