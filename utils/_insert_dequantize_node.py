
def _insert_dequantize_node(node: Node, graph: Graph) -> None:
    """Inserts dequantize node for `node` in `graph`"""
    with graph.inserting_after(node):
        dequantize_node = graph.call_method("dequantize", (node,))
        for user_node in dict(node.users):
            if user_node is not dequantize_node:
                user_node.replace_input_with(node, dequantize_node)

