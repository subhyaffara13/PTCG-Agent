
def get_node_first_ancestor_of_type(
    node: nodes.NodeNG, ancestor_type: type[_NodeT] | tuple[type[_NodeT], ...]
) -> _NodeT | None:
    """Return the first parent node that is any of the provided types (or None)."""
    for ancestor in node.node_ancestors():
        if isinstance(ancestor, ancestor_type):
            return ancestor  # type: ignore[no-any-return]
    return None

