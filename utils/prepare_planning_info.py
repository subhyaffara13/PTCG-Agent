
def prepare_planning_info(
    nodes: list[BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
    name_to_fused_node: dict[str, BaseSchedulerNode],
    graph_inputs: OrderedSet[str],
    graph_outputs: OrderedSet[str],
) -> tuple[int, dict[str, FreeableInputBuffer]]:
    """
    Prepare planning info. As nodes are scheduled one at a time, these help
    keep track of when a buffer can be freed, and when a node can be scheduled

    Returns:
        int: peak memory estimation
        dict[str, FreeableInputBuffer]: name to freeable input buffer
    """
    name_to_freeable_input_buf = get_freeable_input_buf(nodes, graph_inputs)
    assign_memory_planning_info_for_scheduler_buffers(nodes, name_to_buf)
    assign_memory_planning_info_for_scheduler_nodes(
        nodes, name_to_fused_node, name_to_buf, name_to_freeable_input_buf
    )

    # the default
    estimated_peak_memory, _ = estimate_peak_memory(
        nodes, name_to_freeable_input_buf, graph_outputs
    )

    return estimated_peak_memory, name_to_freeable_input_buf

