
def _collect_backward_region_data(
    gm: fx.GraphModule,
) -> tuple[bool, int | None, int | None, int]:
    use_phase = _has_user_phase_annotation(gm)
    bwd_start: int | None = None
    bwd_end: int | None = None
    num_regions = 0
    in_backward = False

    for idx, node in enumerate(gm.graph.nodes):
        is_bwd = _is_backward_node(node, use_phase=use_phase)
        if is_bwd:
            if bwd_start is None:
                bwd_start = idx
            bwd_end = idx + 1
            if not in_backward:
                num_regions += 1
        in_backward = is_bwd

    return use_phase, bwd_start, bwd_end, num_regions

