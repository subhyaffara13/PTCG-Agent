
def _default_root_node_getter(node_pattern):
    if node_pattern is None:
        return node_pattern
    while not isinstance(node_pattern, Node):
        node_pattern = node_pattern[-1]
    return node_pattern

