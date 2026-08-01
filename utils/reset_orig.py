
def reset_orig():
    """Restore all RC params to original settings (respects custom rc)."""
    from . import _orig_rc_params
    mpl.rcParams.update(_orig_rc_params)

