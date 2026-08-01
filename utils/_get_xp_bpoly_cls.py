
def _get_xp_bpoly_cls(xp):
    """Returns bpoly class to delegate to for xp along with internal array namespace.

    Parameters
    ----------
    xp : module

    Returns
    -------
    cls : type
        The bpoly class to delegate to for namespace `xp`.
    namespace : module
        The internal namespace that calculations are performed with
        (may differ from `xp`, e.g. numpy delegation for torch on CPU).
    """
    # A device kwarg could be added to give device dependent delegation
    # e.g., delegating torch to numpy on CPU and cupy on GPU.
    if is_numpy(xp):
        return _BPoly, xp
    spx = scipy_namespace_for(xp)
    cls = getattr(getattr(spx, "interpolate", None), "BPoly", None)
    if cls is not None:
        return cls, xp
    return _BPoly, np

