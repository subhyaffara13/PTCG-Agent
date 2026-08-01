
def is_base_container(node: nodes.NodeNG | None) -> bool:
    return isinstance(node, nodes.BaseContainer) and not node.elts

