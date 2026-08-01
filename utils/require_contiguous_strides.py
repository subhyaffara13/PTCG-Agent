
def require_contiguous_strides(_, *args, **kwargs):
    # TODO: combine this with require_contiguous after
    # https://github.com/pytorch/pytorch/pull/148235 lands.
    args, kwargs = pytree.tree_map_only(
        _is_tensor_irnode,
        ir.ExternKernel.require_contiguous_strides,
        (args, kwargs),
    )
    return args, kwargs

