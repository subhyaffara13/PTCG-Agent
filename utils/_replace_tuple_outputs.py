
def _replace_tuple_outputs(
    node: Node,
    output_index: int,
    tuple_spec: dict[tuple[int, ...], int],
    invoke_subgraph_node: Node,
    graph: torch.fx.Graph,
) -> OrderedSet[Node]:
    assert _is_tuple_node(node), "_replace_tuple_outputs expects a tuple node"

    queue = deque((c, (c.args[1],)) for c in _get_children_getitems(node))
    erased_nodes: OrderedSet[Node] = OrderedSet()
    while queue:
        cur_node, path = queue.pop()

        for c in _get_children_getitems(cur_node):
            queue.append((c, path + (c.args[1],)))  # type: ignore[return-value, arg-type]

        with graph.inserting_after(invoke_subgraph_node):
            subgraph_output = graph.create_node(
                "call_function",
                operator.getitem,
                (invoke_subgraph_node, output_index + tuple_spec[path]),  # type: ignore[index]
                {},
            )
        cur_node.replace_all_uses_with(subgraph_output, propagate_meta=True)
        graph.erase_node(cur_node)
        erased_nodes.add(cur_node)

    graph.erase_node(node)
    erased_nodes.add(node)
    return erased_nodes

