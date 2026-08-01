
def register_dispatch_func(aten_ops):
    """
    Used for registering a new __torch_dispatch__ function to MaskedTensor
    Called via _MASKEDTENSOR_DISPATCH_TABLE[func](*args, **kwargs)

    The code to register a new function looks like:

    @register_dispatch_func(list_of_ops)
    def foo(func, *args, **kwargs):
        <implementation>
    """

    def wrapper(func):
        for aten_op in aten_ops:
            _MASKEDTENSOR_DISPATCH_TABLE[aten_op] = partial(func, aten_op)

    return wrapper

