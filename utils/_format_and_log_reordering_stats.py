
def _format_and_log_reordering_stats(
    stats: dict[BaseSchedulerNode, ReorderInfo],
    head: BaseSchedulerNode,
    next_dict: dict[BaseSchedulerNode, BaseSchedulerNode | None],
    original_snodes_num: int,
    peak_memory: int,
    name_to_freeable_input_buf: dict,
    graph_outputs: OrderedSet[str],
) -> list[BaseSchedulerNode]:
    """
    Format reordering statistics, log them, and return final node list.

    Computes improvement metrics, creates a formatted table (using tabulate if
    available), validates the reordered node count, recalculates peak memory,
    and logs all information.

    Args:
        stats: Per-node reordering statistics
        head: Head of the reordered linked list
        next_dict: Linked list next pointers
        original_snodes_num: Original number of nodes (for validation)
        peak_memory: Initial peak memory before reordering
        name_to_freeable_input_buf: Buffer memory tracking info
        graph_outputs: Graph output names

    Returns:
        Final reordered list of scheduler nodes
    """
    node_stats = stats
    improvement = {snode: node_stats[snode].improvement for snode in node_stats}
    total_improvement = sum([improvement[snode] for snode in improvement])
    total_moves = sum([node_stats[snode].moves for snode in node_stats])

    reorder_log_str = (
        f"reorder_communication_preserving_peak_memory improved overlap by {total_improvement} ns"
        f" after {total_moves} reorders.\n"
    )
    headers = [
        "Collective node",
        "comm_time(us)",
        "comp_time(us)",
        "initial exposed(us)",
        "final exposed(us)",
        "improvement(us)",
        "limiting factor",
        "moves",
        "grouped",
        "grouped_info",
        "overlap_info",
    ]
    rows = [
        [
            node_summary(snode),
            node_info.comm_time / 1e3,
            node_info.comp_time / 1e3,
            node_info.initial_exposed / 1e3,
            node_info.final_exposed / 1e3,
            node_info.improvement / 1e3,
            node_info.limiting_factor,
            node_info.moves,
            node_info.grouped,
            node_info.grouped_info,
            node_info.overlap_info,
        ]
        for snode, node_info in node_stats.items()
    ]
    if importlib.util.find_spec("tabulate"):
        from tabulate import tabulate

        reorder_log_str += tabulate(
            rows,
            headers=headers,
        )
    else:
        reorder_log_str += (
            "Please `pip install tabulate` to nicely render overlap stats.\n"
        )
        reorder_log_str += str(headers) + "\n"
        reorder_log_str += "\n".join(map(str, rows))

    new_snodes = _group_nodes_from_linked_list(head, None, next_dict)
    assert len(new_snodes) == original_snodes_num
    new_peak_memory, _, _, _ = estimate_peak_memory_allocfree(
        new_snodes, name_to_freeable_input_buf, graph_outputs
    )
    reorder_log_str += f"\n peak_memory_before:{peak_memory}"
    reorder_log_str += f"\n peak_memory_after:{new_peak_memory}"

    overlap_log.info(reorder_log_str)
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "reorder_communication_preserving_peak_memory",
            "encoding": "string",
        },
        payload_fn=lambda: reorder_log_str,
    )

    return new_snodes

