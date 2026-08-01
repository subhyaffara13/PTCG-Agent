
def _find_buffers_with_changed_last_use(
    candidate: BaseSchedulerNode,
    gns: list[BaseSchedulerNode],
    buf_to_snode_last_use: dict,
    candidate_buffer_map: dict[BaseSchedulerNode, OrderedSet],
) -> dict[BaseSchedulerNode, list[FreeableInputBuffer | Any]]:
    """
    Find buffers whose last use will change after swapping candidate with group.

    When we swap [candidate [group]] to [[group] candidate], some buffers that
    were last used by a group node will now be last used by candidate instead.
    This affects memory deallocation timing.

    Args:
        candidate: The node being moved
        gns: Group nodes being swapped with candidate
        buf_to_snode_last_use: Mapping of buffers to their current last-use nodes
        candidate_buffer_map: Pre-computed map of node -> buffers using that node

    Returns:
        Dict mapping group nodes to buffers that will change their last-use node
    """
    group_n_to_bufs_after_swap_dealloc_by_candidate: dict[
        BaseSchedulerNode, list[FreeableInputBuffer | Any]
    ] = defaultdict(list)

    # Optimization: only check buffers where candidate is a successor
    # Reduces from O(all_buffers) to O(buffers_per_candidate)
    candidate_bufs = candidate_buffer_map.get(candidate, OrderedSet())
    gns_set = OrderedSet(gns)  # O(1) membership testing

    for buf in candidate_bufs:
        snode_last_use = buf_to_snode_last_use[buf]
        if snode_last_use in gns_set:
            group_n_to_bufs_after_swap_dealloc_by_candidate[snode_last_use].append(buf)

    return group_n_to_bufs_after_swap_dealloc_by_candidate

