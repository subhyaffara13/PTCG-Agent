
def _format_and_log_sink_waits_stats(
    stats: dict[BaseSchedulerNode, SinkWaitInfo],
    head: BaseSchedulerNode,
    next_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    original_snodes_num: int,
    peak_memory: int,
    name_to_freeable_input_buf: dict,
    graph_outputs: OrderedSet[str],
) -> list[BaseSchedulerNode]:
    """
    Format sink_waits statistics, log them, and return final node list.

    Computes improvement metrics, creates a formatted table (using tabulate if
    available), validates the reordered node count, recalculates peak memory,
    and logs all information.

    Args:
        stats: Per-node sink_waits statistics
        head: Head of the reordered linked list
        next_dict: Linked list next pointers
        original_snodes_num: Original number of nodes (for validation)
        peak_memory: Initial peak memory before reordering
        name_to_freeable_input_buf: Buffer memory tracking info
        graph_outputs: Graph output names

    Returns:
        Final reordered list of scheduler nodes
    """
    headers = [
        "Wait node",
        "comm_time(us)",
        "comp_time(us)",
        "initial exposed(us)",
        "final exposed(us)",
        "improvement(us)",
        "limiting factor",
        "grouped",
        "grouped_info",
        "moves",
        "moves_info",
        "overlap_info",
    ]
    rows = [
        [
            node_summary(snode),
            info.comm_time / 1e3,
            info.comp_time / 1e3,
            info.initial_exposed / 1e3,
            info.final_exposed / 1e3,
            info.improvement / 1e3,
            info.limiting_factor,
            info.grouped,
            info.grouped_info,
            info.moves,
            info.moves_info,
            info.overlap_info,
        ]
        for snode, info in stats.items()
    ]
    log_str = ""
    if importlib.util.find_spec("tabulate"):
        from tabulate import tabulate

        log_str += tabulate(
            rows,
            headers=headers,
        )
    else:
        log_str += "Please `pip install tabulate` to nicely render overlap stats.\n"
        log_str += str(headers) + "\n"
        log_str += "\n".join(map(str, rows))
    overlap_log.info(log_str)
    new_snodes = _group_nodes_from_linked_list(head, None, next_dict)
    assert len(new_snodes) == original_snodes_num
    new_peak_memory, _, _, _ = estimate_peak_memory_allocfree(
        new_snodes, name_to_freeable_input_buf, graph_outputs
    )
    log_str += f"\n sink_waits_iterative peak_memory_before:{peak_memory}"
    log_str += f"\n sink_waits_iterative peak_memory_after:{new_peak_memory}"
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "sink_waits_iterative_info",
            "encoding": "string",
        },
        payload_fn=lambda: log_str,
    )
    return new_snodes

