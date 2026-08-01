
def set_checkpoint_early_stop(enable: bool):
    """Context manager that sets whether checkpoint should stop recomputation early.

    By default, non-reentrant checkpoint stops recomputation as soon as it
    has computed all needed Tensors. This context manager can be used to disable
    that feature if it is problematic for your specific application.

    This context manager only needs to be active when forward is run. It does
    not need to be active during backward.

    Example::

    >>> # xdoctest: +SKIP(failing)
    >>> message = "saved tensors default hooks are disabled"
    >>> with set_checkpoint_early_stop(False):
    ...     # Any checkpoint under this context manager will respect this
    ...     # context manager, even if its backward is performed outside.
    ...     out = checkpoint(fn, inputs)
    ...
    >>> out.backward()
    """
    global _enable_checkpoint_early_stop
    try:
        prev = _enable_checkpoint_early_stop
        _enable_checkpoint_early_stop = enable
        yield
    finally:
        _enable_checkpoint_early_stop = prev

