
def _update_memory_tracking_after_swap_sink_waits(
    candidate: BaseSchedulerNode,
    gns: list[BaseSchedulerNode],
    candidate_delta_mem: int,
    candidate_allocfree: SNodeMemory,
    group_n_to_bufs_after_swap_dealloc_instead_of_candidate: dict,
    post_alloc_update: dict[BaseSchedulerNode, int],
    size_free_delta_update: dict[BaseSchedulerNode, int],
    curr_memory: dict,
    snodes_allocfree: dict,
) -> None:
    """
    Update memory tracking structures after swap (sink_waits version).

    Updates curr_memory and snodes_allocfree dictionaries to reflect the new
    memory state after swapping candidate with group.

    Args:
        candidate: Node that was moved
        gns: Group nodes
        candidate_delta_mem: Net memory change from candidate (alloc - free)
        candidate_allocfree: Candidate's allocation/free info
        group_n_to_bufs_after_swap_dealloc_instead_of_candidate: Buffers whose deallocation moves from candidate to group
        post_alloc_update: Cached post-allocation memory values
        size_free_delta_update: Cached size-free delta values
        curr_memory: Current memory state dict (mutated)
        snodes_allocfree: Node allocation/free info dict (mutated)
    """
    group_head = gns[0]
    pre_group_mem = curr_memory[group_head][0] - snodes_allocfree[group_head].size_alloc
    if not group_n_to_bufs_after_swap_dealloc_instead_of_candidate:
        candidate_post_alloc = pre_group_mem + candidate_allocfree.size_alloc
        curr_memory[candidate] = (
            candidate_post_alloc,
            candidate_post_alloc - candidate_allocfree.size_free,
        )
        for gn in gns:
            cm = curr_memory[gn]
            curr_memory[gn] = (
                cm[0] + candidate_delta_mem,
                cm[1] + candidate_delta_mem,
            )
        return

    for n in [candidate, *gns]:
        post_alloc = post_alloc_update[n]
        snodes_allocfree[n].size_free += size_free_delta_update.get(n, 0)
        curr_memory[n] = (
            post_alloc,
            post_alloc - snodes_allocfree[n].size_free,
        )

