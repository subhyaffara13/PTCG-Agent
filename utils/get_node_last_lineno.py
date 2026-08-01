
def get_node_last_lineno(node: nodes.NodeNG) -> int:
    """Get the last lineno of the given node.

    For a simple statement this will just be node.lineno,
    but for a node that has child statements (e.g. a method) this will be the lineno of the last
    child statement recursively.
    """
    # 'finalbody' is always the last clause in a try statement, if present
    if getattr(node, "finalbody", False):
        return get_node_last_lineno(node.finalbody[-1])
    # For if, while, and for statements 'orelse' is always the last clause.
    # For try statements 'orelse' is the last in the absence of a 'finalbody'
    if getattr(node, "orelse", False):
        return get_node_last_lineno(node.orelse[-1])
    # try statements have the 'handlers' last if there is no 'orelse' or 'finalbody'
    if getattr(node, "handlers", False):
        return get_node_last_lineno(node.handlers[-1])
    # All compound statements have a 'body'
    if getattr(node, "body", False):
        return get_node_last_lineno(node.body[-1])
    # Not a compound statement
    return node.lineno  # type: ignore[no-any-return]

