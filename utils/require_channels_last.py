
def require_channels_last(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        _is_tensor_irnode,
        ir.ExternKernel.require_channels_last,
        (args, kwargs),
    )
    return args, kwargs

