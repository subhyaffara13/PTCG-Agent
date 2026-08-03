import functools

def _get_decomp_for_cia(op: "OperatorBase"):
    # [NOTE] Separating out func.decompose
    # Ideally we should be able to just register func.decompose but
    # we can't as this decomp is gonna be registered to the py_impl.
    # As a result it will infinitely recurse. So we first check if the op
    # has py_impl entry for CIA and if it is we use that first. If not,
    # we register C++ query to py_impl.
    dk = torch._C.DispatchKey.CompositeImplicitAutograd
    if dk in op.py_kernels and not isinstance(op.py_kernels[dk], torch._C.DispatchKey):
        return op.py_kernels[dk]

    def _special_op_to_decompose_cia(*args, **kwargs):
        kernel = kwargs["kernel"]
        del kwargs["kernel"]
        # Can't call kernel.decompose due to infinite recursion as
        # we register this kernel to py_impl directly
        dk = torch._C.DispatchKey.CompositeImplicitAutograd
        if torch._C._dispatch_has_kernel_for_dispatch_key(
            kernel.name(), torch._C.DispatchKey.CompositeImplicitAutograd
        ):
            return kernel._op_dk(dk, *args, **kwargs)
        else:
            raise AssertionError(
                f"Expected {kernel} to have CompositeImplicitAutograd kernel"
            )

    return functools.partial(_special_op_to_decompose_cia, kernel=op)

