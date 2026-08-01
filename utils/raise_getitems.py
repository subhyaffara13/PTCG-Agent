
def raise_getitems(gm: fx.GraphModule) -> fx.GraphModule:
    # Pre-create a list of nodes to iterate over, as modifying the node order
    # during the loop can lead to infinite loops if not handled properly.
    getitem_nodes = list(
        gm.graph.find_nodes(op="call_function", target=operator.getitem)
    )

    # loop through getitem nodes in the graph and raise them to the parent node
    # in reverse order to preserve their original relative order
    for node in reversed(getitem_nodes):
        if len(node.all_input_nodes) != 1:
            raise AssertionError(
                f"expected node {node.name} to have 1 input node, got {len(node.all_input_nodes)}"
            )
        parent = node.all_input_nodes[0]
        parent.append(node)

    gm.recompile()
    return gm

