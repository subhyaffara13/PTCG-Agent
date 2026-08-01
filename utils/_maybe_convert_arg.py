
def _maybe_convert_arg(arg, xp):
    """Convert arrays/scalars hiding in the sequence `arg`."""
    if isinstance(arg, np.ndarray | np.generic):
        return xp.asarray(arg)
    elif isinstance(arg, list | tuple):
        return type(arg)(_maybe_convert_arg(x, xp) for x in arg)
    else:
        return arg

