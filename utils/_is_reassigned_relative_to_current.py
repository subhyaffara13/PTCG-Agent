
def _is_reassigned_relative_to_current(
    node: nodes.NodeNG, varname: str, before: bool
) -> bool:
    """Check if the given variable name is reassigned in the same scope relative to
    the current node.
    """
    node_scope = node.scope()
    node_lineno = node.lineno
    if node_lineno is None:
        return False
    for a in node_scope.nodes_of_class(
        (nodes.AssignName, nodes.ClassDef, nodes.FunctionDef)
    ):
        if a.name == varname and a.lineno is not None:
            if before:
                if a.lineno < node_lineno:
                    if _is_node_in_same_scope(a, node_scope):
                        return True
            elif a.lineno > node_lineno:
                if _is_node_in_same_scope(a, node_scope):
                    return True
    return False

