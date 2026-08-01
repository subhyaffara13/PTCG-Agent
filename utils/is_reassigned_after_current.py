
def is_reassigned_after_current(node: nodes.NodeNG, varname: str) -> bool:
    """Check if the given variable name is reassigned in the same scope after the
    current node.
    """
    return _is_reassigned_relative_to_current(node, varname, before=False)

