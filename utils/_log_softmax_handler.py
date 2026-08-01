
def _log_softmax_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    x = cast(DTensor, args[0])
    dim = cast(int, args[1])
    half_to_float = cast(bool, args[2])

    spec = x._spec
    dim = normalize_dim(dim, x.dim())
    mesh_dim = _find_all_reduce_mesh_dim(spec.placements, dim)

    output_tensor_meta = _propagate_tensor_meta(op_call, args, kwargs)

    res = _log_softmax(x._local_tensor, dim, half_to_float, spec.mesh, mesh_dim)

    res_spec = DTensorSpec(
        spec.mesh,
        spec.placements,
        tensor_meta=output_tensor_meta,
    )

    # pyrefly: ignore [bad-argument-type]
    return DTensor(
        # pyrefly: ignore [bad-argument-count]
        res,
        res_spec,
        # pyrefly: ignore [unexpected-keyword]
        requires_grad=res.requires_grad,
    )

