
def identify_reload_patterns(
    graph: fx.Graph, nodes_list: list[fx.Node], node_to_idx: dict[fx.Node, int]
) -> dict[fx.Node, ReloadNodeInfo]:
    """
    Identify backward reload patterns in the graph.

    Pattern: fork → wait_stream → device_put → record_event → join → wait_event

    This uses position-based matching since these nodes are inserted together in
    add_backward_reload_stream_ops() in a specific order. Since stream operations
    do not have data dependencies between them, they are unsuitable for subgroup
    pattern matching type of checks.

    Returns a dict mapping device_put node to ReloadNodeInfo containing:
    - reload_group_nodes: fork → wait_stream → device_put → record_event → join
    - wait_event_node: the wait_event node
    - transfer_size_bytes: size of data being transferred
    - transfer_time_ms: estimated transfer time in milliseconds
    """
    patterns: dict[fx.Node, ReloadNodeInfo] = {}

    # Find all GPU reload device_put nodes whose inputs are placeholder nodes
    reload_nodes: list[fx.Node] = [
        node
        for node in graph.find_nodes(
            op="call_function", target=torch.ops.prims.device_put.default
        )
        if GPU_RELOAD_PREFIX in node.name
        and (
            node.args
            and isinstance(node.args[0], fx.Node)
            and node.args[0].op == "placeholder"
        )
    ]

    # Extract patterns for each reload device_put node
    for reload_node in reload_nodes:
        reload_node_idx: int = node_to_idx[reload_node]

        fork_node: fx.Node = nodes_list[reload_node_idx - 2]
        wait_stream_node: fx.Node = nodes_list[reload_node_idx - 1]
        record_event_node: fx.Node = nodes_list[reload_node_idx + 1]
        join_node: fx.Node = nodes_list[reload_node_idx + 2]
        wait_event_node: fx.Node = nodes_list[reload_node_idx + 3]

        # Validate the nodes are what we expect
        # Removed in follow-up commit
        _validate_pattern_nodes(  # noqa: F821  # pyrefly: ignore [unknown-name]
            fork_node,
            wait_stream_node,
            record_event_node,
            join_node,
            wait_event_node,
        )

        # Calculate transfer size and time
        transfer_size_bytes: int = _calculate_transfer_size(reload_node)
        transfer_time_ms: float = _estimate_transfer_time_in_ms(transfer_size_bytes)

        patterns[reload_node] = ReloadNodeInfo(
            reload_group_nodes=[
                fork_node,
                wait_stream_node,
                reload_node,
                record_event_node,
                join_node,
            ],
            wait_event_node=wait_event_node,
            transfer_size_bytes=transfer_size_bytes,
            transfer_time_ms=transfer_time_ms,
        )

    return patterns

