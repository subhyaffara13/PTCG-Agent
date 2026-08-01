
def is_func_decorator(node: nodes.NodeNG) -> bool:
    """Return true if the name is used in function decorator."""
    for parent in node.node_ancestors():
        if isinstance(parent, nodes.Decorators):
            return True
        if parent.is_statement or isinstance(
            parent,
            (
                nodes.Lambda,
                nodes.ComprehensionScope,
                nodes.ListComp,
            ),
        ):
            break
    return False

