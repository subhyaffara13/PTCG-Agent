
def rewrite_index_for_function(
    localize_buffer_handler: "LocalizeBufferHandler",
    index: sympy.Expr,
    global_buf_name: str,
):
    # Local buffer at the inner dimensions
    snode = V.graph.scheduler.name_to_buf[global_buf_name].defining_op
    assert snode is not None
    local_buf = localize_buffer_handler.global_to_local[global_buf_name]
    scheduler_nodes = snode.get_nodes()
    _, (group, reduction_group) = max(
        scheduler_nodes, key=lambda x: int(x.is_reduction())
    ).group
    call_ranges = tuple(group) + tuple(reduction_group)
    indices_to_keep = [
        f"x{len(call_ranges) - (idx + 1)}"
        for idx in range(len(local_buf.get_layout().size))
    ]
    sorted_symbols = sorted(index.free_symbols, key=lambda s: s.name)  # type: ignore[attr-defined]
    replacements = {}
    for x in sorted_symbols:
        if x.name.startswith("x") and x.name not in indices_to_keep:  # type: ignore[attr-defined]
            # Only keep index used by local buffer
            replacements[x] = sympy.core.numbers.Zero()
    index = sympy_subs(index, replacements)  # type: ignore[arg-type]
    return index

