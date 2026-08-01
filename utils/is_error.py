
def is_error(node: nodes.FunctionDef) -> bool:
    """Return true if the given function node only raises an exception."""
    return len(node.body) == 1 and isinstance(node.body[0], nodes.Raise)

