
def get_node_first_ancestor_of_type_and_its_child(
    node: nodes.NodeNG, ancestor_type: type[_NodeT] | tuple[type[_NodeT], ...]
) -> tuple[None, None] | tuple[_NodeT, nodes.NodeNG]:
    """Modified version of get_node_first_ancestor_of_type to also return the
    descendant visited directly before reaching the sought ancestor.

    Useful for extracting whether a statement is guarded by a try, except, or finally
    when searching for a Try ancestor.
    """
    child = node
    for ancestor in node.node_ancestors():
        if isinstance(ancestor, ancestor_type):
            return (ancestor, child)
        child = ancestor
    return None, None

