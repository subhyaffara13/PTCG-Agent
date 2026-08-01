
def _create_getitem_nodes(
    node: Node, subgraph_tuple_node: Node, subgraph: torch.fx.Graph
) -> tuple[list[Node], dict[tuple[int, ...], int]]:
    tup = node.meta["example_value"]
    assert isinstance(tup, tuple), "_get_getitem_children expects tuple"

    getitem_nodes: list[Node] = []
    queue = deque([(e, (i,), subgraph_tuple_node) for i, e in enumerate(tup)])
    path_to_output_index = {}

    while queue:
        cur_elem, path, parent = queue.popleft()

        with subgraph.inserting_after(parent):
            new_getitem_node = subgraph.create_node(
                "call_function", operator.getitem, (parent, path[-1]), {}
            )
        new_getitem_node.meta["example_value"] = cur_elem

        path_to_output_index[path] = len(getitem_nodes)
        getitem_nodes.append(new_getitem_node)

        if isinstance(cur_elem, tuple):
            queue.extend(
                [(e, path + (i,), new_getitem_node) for i, e in enumerate(cur_elem)]  # type: ignore[arg-type,misc]
            )

    return getitem_nodes, path_to_output_index  # type: ignore[return-value]

