
def _get_if_statement_ancestor(node: nodes.NodeNG) -> nodes.If | None:
    """Return the first parent node that is an If node (or None)."""
    for parent in node.node_ancestors():
        if isinstance(parent, nodes.If):
            return parent
    return None

