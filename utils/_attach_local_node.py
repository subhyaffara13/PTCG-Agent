
def _attach_local_node(parent, node, name: str) -> None:
    node.name = name  # needed by add_local_node
    parent.add_local_node(node)

