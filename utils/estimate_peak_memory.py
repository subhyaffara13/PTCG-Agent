
def estimate_peak_memory(
    nodes: list[BaseSchedulerNode],
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer],
    graph_outputs: OrderedSet[str],
) -> tuple[int, list[int]]:
    """
    Given a list of nodes in their execution order, estimate the peak memory, by
    keeping track of the liveliness of SchedulerBuffers and FreeableInputBuffers.

    Returns:
        int: peak memory
        List[int]: memory usage at each node (or each step).
    """

    buf_info_list, _, _ = compute_memory_timeline(
        nodes, name_to_freeable_input_buf, graph_outputs
    )

    # incremental memory changes at each step
    memory = [0 for _ in range(len(nodes) + 1)]

    # for each buffer, update memory when created and when freed
    for buf_info in buf_info_list:
        memory[buf_info.start_step] += buf_info.size_alloc
        memory[buf_info.end_step + 1] -= buf_info.size_free

    # get peak memory by compute the cumulative memories
    max_memory = 0
    cur_memory = 0
    memories_at_nodes = []
    for t in range(len(nodes) + 1):
        cur_memory += memory[t]
        memories_at_nodes.append(cur_memory)
        max_memory = max(max_memory, cur_memory)

    return (max_memory, memories_at_nodes)

