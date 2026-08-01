
def _insert_copy_of_subgraph_a_after_input_node_c(
    input_node_c: Node | list[Node],
    input_node_c_2: Node | list[Node] | None,
    subgraph_a: NSSubgraph,
    gm_a: GraphModule,
    gm_b: GraphModule,
    node_name_prefix: str,
) -> Node:
    """
    TODO(before land): real docblock
    """
    if not isinstance(input_node_c, (Node, list)):
        raise AssertionError(f"Expected Node or list, got {type(input_node_c)}")

    # create a sequential list of the subgraphs' nodes from start to end,
    # because we need to add the nodes to graph C in non-reverse order
    nodes_of_a = [subgraph_a.end_node]
    cur_node = subgraph_a.end_node
    while cur_node != subgraph_a.start_node:
        cur_node = get_normalized_nth_input(cur_node, gm_a, 0)  # type: ignore[assignment]
        nodes_of_a.insert(0, cur_node)

    # go through nodes of a in order, and insert them into the graph of c
    # sequentially
    cur_node_a = nodes_of_a[0]
    cur_node_c = _insert_copy_of_node_a_after_input_node_c(
        input_node_c, input_node_c_2, cur_node_a, gm_a, gm_b, node_name_prefix
    )
    for cur_idx_a in range(1, len(nodes_of_a)):
        cur_node_a = nodes_of_a[cur_idx_a]
        prev_node_c = cur_node_c  # previous added node is the input to next node
        cur_node_c = _insert_copy_of_node_a_after_input_node_c(
            prev_node_c,
            # TODO(future PR): enable multiple inputs for nodes which are not at start of subgraph
            None,
            cur_node_a,
            gm_a,
            gm_b,
            node_name_prefix,
        )
    # return the last inserted node
    return cur_node_c

