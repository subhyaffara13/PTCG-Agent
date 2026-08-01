
def _is_cia_op(op: "OperatorBase") -> bool:
    return (
        torch._C._dispatch_has_kernel_for_dispatch_key(
            op.name(), torch._C.DispatchKey.CompositeImplicitAutograd
        )
        or torch._C.DispatchKey.CompositeImplicitAutograd in op.py_kernels
    )

