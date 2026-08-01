
def is_dequantize_node(node):
    return (
        isinstance(node, Node)
        and node.op == "call_method"
        and node.target == "dequantize"
    )

