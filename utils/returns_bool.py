
def returns_bool(node: nodes.NodeNG) -> bool:
    """Returns true if a node is a nodes.Return that returns a constant boolean."""
    match node:
        case nodes.Return(value=nodes.Const(value=bool())):
            return True
    return False

