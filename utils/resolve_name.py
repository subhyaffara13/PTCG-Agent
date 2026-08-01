
def resolve_name(f):
    """Get a human readable string name for a function passed to
    __torch_function__

    Arguments
    ---------
    f : Callable
        Function to resolve the name of.

    Returns
    -------
    str
        Name of the function; if eval'ed it should give back the input
        function.
    """
    if isinstance(f, (torch._ops.OpOverload, torch._ops.OpOverloadPacket)):
        return str(f)
    return _get_overridable_functions()[1].get(f)

