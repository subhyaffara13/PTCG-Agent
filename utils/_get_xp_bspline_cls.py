
def _get_xp_bspline_cls(xp):
    """Returns bspline class to delegate to for xp along with internal array namespace.

    Parameters
    ----------
    xp : module

    Returns
    -------
    cls : type
        The bspline class to delegate to for namespace `xp`.
    namespace : module
        The internal namespace that calculations are performed with
        (may differ from `xp`, e.g. numpy delegation for torch on CPU).
    """
    # A device kwarg could be added to give device dependent delegation
    # e.g., delegating torch to numpy on CPU and cupy on GPU.
    if is_numpy(xp):
        return _BSpline, xp
    spx = scipy_namespace_for(xp)
    cls = getattr(getattr(spx, "interpolate", None), "BSpline", None)
    if cls is not None:
        return cls, xp
    return _BSpline, np

