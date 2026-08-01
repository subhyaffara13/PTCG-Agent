
def propagate_requires_no_scaling(out_node: Node) -> bool:
    """
    For nonlinear ops (exp, log, tanh) scale_by cannot be propagated
    through since f(S*x) != S*f(x). For boolean-output ops (eq) scale_by
    is meaningless. These ops only appear in the chunking subgraph when
    scale_by is None (e.g. the final gradient is 1).
    """
    args_node = get_args_of_node_type(out_node)
    args_meta = get_chunking_metas(args_node)
    out_meta = get_chunking_meta(out_node)

    scale_by = get_scale_by_from_metas(*args_meta)  # type: ignore[arg-type]
    assert scale_by is None, (
        f"Nonlinear op {out_node.target} requires scale_by=None, got {scale_by}"
    )
    assert out_meta is not None
    out_meta.scale_by = None
    return True

