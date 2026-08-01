
def _calculate_potential_peak_memory_reorder(
    candidate: BaseSchedulerNode,
    gns: list[BaseSchedulerNode],
    group_tail: BaseSchedulerNode,
    group_peak_memory: int,
    candidate_delta_mem: int,
    candidate_allocfree: SNodeMemory,
    group_n_to_bufs_after_swap_dealloc_by_candidate: dict,
    curr_memory: dict,
) -> tuple[int, dict[BaseSchedulerNode, int]]:
    """
    Calculate potential peak memory after swapping candidate with group (reorder version).

    Computes new memory levels for all affected nodes and returns the potential
    peak memory along with cached post-allocation memory values for each node.

    Args:
        candidate: Node being moved
        gns: Group nodes
        group_tail: Last node of group
        group_peak_memory: Current peak memory within the group
        candidate_delta_mem: Net memory change from candidate (alloc - free)
        candidate_allocfree: Candidate's allocation/free info
        group_n_to_bufs_after_swap_dealloc_by_candidate: Buffers whose deallocation moves to candidate
        curr_memory: Current memory state dict

    Returns:
        Tuple of (potential_peak_memory, post_alloc_update_dict)
    """
    # Caching calculations of memory for group nodes and candidate,
    # to apply without recalculation after swap.
    _post_alloc_update: dict[BaseSchedulerNode, int] = {}
    potential_peak: int = 0
    if not group_n_to_bufs_after_swap_dealloc_by_candidate:
        # Not accounting for buffers last use change
        potential_peak = max(
            group_peak_memory - candidate_delta_mem,
            curr_memory[group_tail][1]
            - candidate_delta_mem
            + candidate_allocfree.size_alloc,
        )
        return potential_peak, _post_alloc_update

    # If candidate will be after group, the starting memory level of group nodes
    # changes to the -(candidate.size_alloc - candidate.size_free)
    mem_after_reorder_delta: int = -candidate_delta_mem
    for gn in gns:
        gn_post_alloc_mem = curr_memory[gn][0] + mem_after_reorder_delta
        _post_alloc_update[gn] = gn_post_alloc_mem
        potential_peak = max(potential_peak, gn_post_alloc_mem)

        bufs = group_n_to_bufs_after_swap_dealloc_by_candidate.get(gn)
        if bufs is not None:
            for buf in bufs:
                # Candidate will deallocate those buffers
                mem_after_reorder_delta += buf.mpi_buffer.size_free

    candidate_mem_post_alloc = (
        curr_memory[group_tail][1]
        + mem_after_reorder_delta
        + candidate_allocfree.size_alloc
    )
    _post_alloc_update[candidate] = candidate_mem_post_alloc
    potential_peak = max(potential_peak, candidate_mem_post_alloc)
    return potential_peak, _post_alloc_update

