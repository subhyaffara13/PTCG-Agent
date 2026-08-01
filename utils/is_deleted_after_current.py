
def is_deleted_after_current(node: nodes.NodeNG, varname: str) -> bool:
    """Check if the given variable name is deleted in the same scope after the current
    node.
    """
    return any(
        getattr(target, "name", None) == varname and target.lineno > node.lineno
        for del_node in node.scope().nodes_of_class(nodes.Delete)
        for target in del_node.targets
    )

