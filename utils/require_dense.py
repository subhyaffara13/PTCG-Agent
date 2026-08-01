
def require_dense(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        _is_tensor_irnode, ir.ExternKernel.require_stride1, (args, kwargs)
    )
    return args, kwargs

