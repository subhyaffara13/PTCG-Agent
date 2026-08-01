
def _is_ellipsis(node: nodes.NodeNG) -> bool:
    return isinstance(node, nodes.Const) and node.value == Ellipsis

