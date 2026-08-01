
def impl_save_for_backward(qualname, *, func=None):
    r"""Register a function that tells us what to save for backward.

    Please see :func:`impl_backward` for more details.
    """

    def inner(func):
        custom_op = _find_custom_op(qualname, also_check_torch_library=True)
        custom_op.impl_save_for_backward(_stacklevel=3)(func)
        return func

    if func is None:
        return inner
    return inner(func)

