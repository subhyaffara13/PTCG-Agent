
def reference_signal_window(fn: Callable):
    r"""Wrapper for scipy signal window references.

    Discards keyword arguments for window reference functions that don't have a matching signature with
    torch, e.g., gaussian window.
    """

    def _fn(
        *args,
        dtype=numpy.float64,
        device=None,
        layout=torch.strided,
        requires_grad=False,
        **kwargs,
    ):
        r"""The unused arguments are defined to disregard those values"""
        return fn(*args, **kwargs).astype(dtype)

    return _fn

