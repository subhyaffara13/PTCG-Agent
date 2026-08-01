
def estimate_peak_memory_allocfree(
    nodes: list[BaseSchedulerNode],
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer],
    graph_outputs: OrderedSet[str],
) -> tuple[
    int,
    list[tuple[int, int]],
    dict[BaseSchedulerNode, SNodeMemory],
    dict[FreeableInputBuffer | SchedulerBuffer, BaseSchedulerNode],
]:
    """
    Alternative version of estimate_peak_memory, that respects the fact,
    that every SchedulerNode has multiple phases:
    1. alloc ( outputs )
    2. run_kernel
    3. dealloc last_use buffers
    estimate_peak_memory collapses memory into one value: size_alloc - size_free
    While peak memory happens after alloc.

    Duplicating the code to not migrate all callsites at once,
    In future usages of estimate_peak_memory will migrate to this version.
    """

    buf_info_list, _, buf_to_snode_last_use = compute_memory_timeline(
        nodes, name_to_freeable_input_buf, graph_outputs
    )

    # incremental memory changes at each step
    step_idx_allocfree = [SNodeMemory(0, 0) for _ in range(len(nodes))]

    # for each buffer, update memory when created and when freed
    for buf_info in buf_info_list:
        step_idx_allocfree[buf_info.start_step].size_alloc += buf_info.size_alloc
        if buf_info.end_step != -1:
            step_idx_allocfree[buf_info.end_step].size_free += buf_info.size_free

    snodes_allocfree = {}
    for i, node in enumerate(nodes):
        snodes_allocfree[node] = step_idx_allocfree[i]

    max_memory = 0
    cur_memory = 0
    snodes_curr_memory = []
    for t in range(len(nodes)):
        alloc = step_idx_allocfree[t].size_alloc
        free = step_idx_allocfree[t].size_free
        cur_memory += alloc
        post_alloc = cur_memory
        max_memory = max(max_memory, cur_memory)
        cur_memory -= free
        post_free = cur_memory
        snodes_curr_memory.append((post_alloc, post_free))

    return (
        max_memory,
        snodes_curr_memory,
        snodes_allocfree,
        buf_to_snode_last_use,
    )

