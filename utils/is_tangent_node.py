
def is_tangent_node(node: Node) -> bool:
    return node.op == "placeholder" and "tangent" in node.name

