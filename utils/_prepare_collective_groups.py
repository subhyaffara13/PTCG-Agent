
def _prepare_collective_groups(
    process_group_so: ScriptObject | ProcessGroup,
) -> tuple[list[int], list[int], int]:
    process_group = (
        ProcessGroup.unbox(process_group_so)
        if isinstance(process_group_so, ScriptObject)
        else process_group_so
    )

    ranks = torch.distributed.get_process_group_ranks(process_group)
    if not ranks:
        raise AssertionError
    # TODO: We can handle permutations but the layout inference algorithm will
    # lose the permutation so we will have to reapply it
    if ranks != sorted(ranks):
        raise AssertionError(ranks)
    offset = ranks[0]
    ranks = [r - offset for r in ranks]

    shape, strides = _indices_to_layout(ranks)
    layout = _MeshLayout(shape, strides)

    global_pg = _get_default_group()
    group_offsets = layout.complement(global_pg.size()).all_ranks_from_zero()

    return ranks, group_offsets, offset

