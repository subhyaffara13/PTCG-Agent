
def activation_reload_prefetch_async(bwd_module: fx.GraphModule) -> None:
    """
    Prefetch backward reload operations by moving ao.reload nodes earlier
    in the graph to overlap data transfer with computation, while keeping
    ao.wait_tensor at its original position.
    """
    graph: fx.Graph = bwd_module.graph
    nodes_list: list[fx.Node] = list(graph.nodes)

    # Identify reload + wait pairs
    reload_patterns: dict[fx.Node, ReloadNodeInfo] = {}
    for node in graph.nodes:
        if not (
            node.op == "call_function" and node.target == torch.ops.ao.reload.default
        ):
            continue
        wait_node = next(
            (u for u in node.users if u.target == torch.ops.ao.wait_tensor.default),
            None,
        )
        if wait_node is None:
            continue
        transfer_size_bytes: int = _calculate_transfer_size(node)
        transfer_time_ms: float = _estimate_transfer_time_in_ms(transfer_size_bytes)
        reload_patterns[node] = ReloadNodeInfo(
            reload_group_nodes=[node],
            wait_event_node=wait_node,
            transfer_size_bytes=transfer_size_bytes,
            transfer_time_ms=transfer_time_ms,
        )

    reorder_for_prefetch(nodes_list, reload_patterns)

