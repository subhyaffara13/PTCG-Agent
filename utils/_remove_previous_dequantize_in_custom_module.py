
def _remove_previous_dequantize_in_custom_module(
    node: Node, prev_node: Node, graph: Graph
) -> None:
    """
    Given a custom module `node`, if the previous node is a dequantize, reroute the custom as follows:

    Before: quantize - dequantize - custom_module
    After: quantize - custom_module
                 \\ - dequantize
    """
    # expecting the input node for a custom module node to be a Node
    if not isinstance(prev_node, Node):
        raise AssertionError(
            f"Expecting the argument for custom module node to be a Node, but got {prev_node}"
        )
    if prev_node.op == "call_method" and prev_node.target == "dequantize":
        node.replace_input_with(prev_node, prev_node.args[0])
        # Remove the dequantize node if it doesn't have other users
        if len(prev_node.users) == 0:
            graph.erase_node(prev_node)

