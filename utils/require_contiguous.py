
def require_contiguous(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        _is_tensor_irnode,
        ir.ExternKernel.require_contiguous,
        (args, kwargs),
    )
    return args, kwargs

