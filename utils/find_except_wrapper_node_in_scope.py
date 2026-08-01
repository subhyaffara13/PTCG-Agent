
def find_except_wrapper_node_in_scope(
    node: nodes.NodeNG,
) -> nodes.ExceptHandler | None:
    """Return the ExceptHandler in which the node is, without going out of scope."""
    for current in node.node_ancestors():
        match current:
            case nodes.LocalsDictNodeNG():
                # If we're inside a function/class definition, we don't want to keep checking
                # higher ancestors for `except` clauses, because if these exist, it means our
                # function/class was defined in an `except` clause, rather than the current code
                # actually running in an `except` clause.
                return None
            case nodes.ExceptHandler():
                return current
    return None

