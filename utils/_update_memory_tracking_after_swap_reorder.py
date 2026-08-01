
def _update_memory_tracking_after_swap_reorder(
    candidate: BaseSchedulerNode,
    gns: list[BaseSchedulerNode],
    group_tail: BaseSchedulerNode,
    candidate_delta_mem: int,
    candidate_allocfree: SNodeMemory,
    group_n_to_bufs_after_swap_dealloc_by_candidate: dict,
    post_alloc_update: dict[BaseSchedulerNode, int],
    curr_memory: dict,
    buf_to_snode_last_use: dict,
    snodes_allocfree: dict,
) -> None:
    """
    Update memory tracking structures after swap (reorder version).

    Updates curr_memory, buf_to_snode_last_use, and snodes_allocfree dictionaries
    to reflect the new memory state after swapping candidate with group.

    Args:
        candidate: Node that was moved
        gns: Group nodes
        group_tail: Last node of group
        candidate_delta_mem: Net memory change from candidate (alloc - free)
        candidate_allocfree: Candidate's allocation/free info
        group_n_to_bufs_after_swap_dealloc_by_candidate: Buffers whose deallocation moves to candidate
        post_alloc_update: Cached post-allocation memory values
        curr_memory: Current memory state dict (mutated)
        buf_to_snode_last_use: Buffer to last-use node mapping (mutated)
        snodes_allocfree: Node allocation/free info dict (mutated)
    """
    if not group_n_to_bufs_after_swap_dealloc_by_candidate:
        for gn in gns:
            cm = curr_memory[gn]
            curr_memory[gn] = (
                cm[0] - candidate_delta_mem,
                cm[1] - candidate_delta_mem,
            )
        _candidate_post_alloc_mem = (
            curr_memory[group_tail][1] + candidate_allocfree.size_alloc
        )
        _candidate_post_free_mem = (
            _candidate_post_alloc_mem - candidate_allocfree.size_free
        )
        curr_memory[candidate] = (
            _candidate_post_alloc_mem,
            _candidate_post_free_mem,
        )
        return

    # Candidate becomes last use of some bufs
    for bufs in group_n_to_bufs_after_swap_dealloc_by_candidate.values():
        for buf in bufs:
            buf_to_snode_last_use[buf] = candidate

    size_free_to_move_to_candidate_sum: int = 0
    for n in gns:
        _gn_post_alloc_mem: int = post_alloc_update[n]
        size_free_to_move_to_candidate: int = sum(
            buf.mpi_buffer.size_free
            for buf in group_n_to_bufs_after_swap_dealloc_by_candidate[n]
        )
        size_free_to_move_to_candidate_sum += size_free_to_move_to_candidate
        # group node does not deallocate this after swap
        snodes_allocfree[n].size_free -= size_free_to_move_to_candidate
        gn_post_free_mem: int = _gn_post_alloc_mem - snodes_allocfree[n].size_free
        curr_memory[n] = (_gn_post_alloc_mem, gn_post_free_mem)
    _candidate_post_alloc_mem = post_alloc_update[candidate]
    snodes_allocfree[candidate].size_free += size_free_to_move_to_candidate_sum
    candidate_post_free_mem = (
        _candidate_post_alloc_mem - snodes_allocfree[candidate].size_free
    )
    curr_memory[candidate] = (
        _candidate_post_alloc_mem,
        candidate_post_free_mem,
    )

