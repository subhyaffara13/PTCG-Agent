
def _is_tuple_node(node: Node) -> bool:
    return isinstance(node.meta["example_value"], tuple)

