
def redirect_to_mode(hop: OperatorBase, mode):
    """Utility for redispatching HOP to underlying mode

    Args:
        hop: The HOP to redispatch
        mode: The mode to redispatch to

    Returns:
        A decorated function that implements the HOP for the given mode
    """

    @hop.py_impl(mode)
    def impl(mode, *args, **kwargs):
        return mode.__torch_dispatch__(hop, [], args, kwargs)

    return impl

