
def is_reassigned_before_current(node: nodes.NodeNG, varname: str) -> bool:
    """Check if the given variable name is reassigned in the same scope before the
    current node.
    """
    return _is_reassigned_relative_to_current(node, varname, before=True)

