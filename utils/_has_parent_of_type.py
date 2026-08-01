
def _has_parent_of_type(
    node: nodes.Call,
    node_type: nodes.Keyword | nodes.Starred,
    statement: _base_nodes.Statement,
) -> bool:
    """Check if the given node has a parent of the given type."""
    parent = node.parent
    while not isinstance(parent, node_type) and statement.parent_of(parent):
        parent = parent.parent
    return isinstance(parent, node_type)

