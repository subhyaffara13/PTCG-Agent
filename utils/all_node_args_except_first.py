
def all_node_args_except_first(node: Node) -> list[int]:
    """
    Returns all node arg indices after first
    """
    return list(range(1, len(node.args)))

