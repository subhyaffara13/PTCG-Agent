
def _remove_profiler_ops(graph: torch.fx.Graph) -> None:
    """
    Remove profiler ops (record_function) from the graph.
    These ops are side-effectful but don't affect computation,
    and we don't want them to block fusion.
    """
    profiler_ops = OrderedSet(
        [
            torch.ops.profiler._record_function_enter.default,
            torch.ops.profiler._record_function_enter_new.default,
            torch.ops.profiler._record_function_exit._RecordFunction,
        ]
    )

    nodes_to_remove = []

    for node in graph.nodes:
        if node.op == "call_function" and node.target in profiler_ops:
            nodes_to_remove.append(node)

    for node in reversed(nodes_to_remove):
        graph.erase_node(node)

