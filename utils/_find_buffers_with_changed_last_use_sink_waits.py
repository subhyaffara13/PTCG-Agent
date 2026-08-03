from typing import Any

def _find_buffers_with_changed_last_use_sink_waits(
    candidate: BaseSchedulerNode,
    gns: list[BaseSchedulerNode],
    buf_to_snode_last_use: dict,
    candidate_buffer_map: dict[BaseSchedulerNode, OrderedSet],
) -> dict[BaseSchedulerNode, list[FreeableInputBuffer | Any]]:
    """
    Find buffers whose last use will change after swapping in sink_waits pass.

    When we swap [group] candidate to candidate [group], some buffers that
    were last used by candidate will now be last used by a group node instead.
    This is the opposite direction from the reorder version.

    Args:
        candidate: The node being moved (currently last use)
        gns: Group nodes being swapped with candidate
        buf_to_snode_last_use: Mapping of buffers to their current last-use nodes
        candidate_buffer_map: Pre-computed map of node -> buffers using that node

    Returns:
        Dict mapping group nodes to buffers that will change their last-use node
    """
    group_n_to_bufs_after_swap_dealloc_instead_of_candidate: dict[
        BaseSchedulerNode, list[FreeableInputBuffer | Any]
    ] = defaultdict(list)

    # Optimization: only check buffers where candidate is a successor
    # Reduces from O(all_buffers) to O(buffers_per_candidate)
    candidate_bufs = candidate_buffer_map.get(candidate, OrderedSet())

    for buf in candidate_bufs:
        snode_last_use = buf_to_snode_last_use[buf]
        if snode_last_use != candidate:  # noqa: E711
            continue

        # candidate is last use of buf
        # Find last group node in successors (maintains order)
        succ_nodes = buf.mpi_buffer.succ_nodes
        last_succ_gn = None
        for gn in gns:
            if gn in succ_nodes:
                last_succ_gn = gn

        if last_succ_gn is None:
            continue

        # gn has successors of buf that after potential swap will become
        # last use of buf and start deallocating buf instead of candidate
        group_n_to_bufs_after_swap_dealloc_instead_of_candidate[last_succ_gn].append(
            buf
        )

    return group_n_to_bufs_after_swap_dealloc_instead_of_candidate

