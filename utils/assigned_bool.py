
def assigned_bool(node: nodes.NodeNG) -> bool:
    """Returns true if a node is a nodes.Assign that returns a constant boolean."""
    match node:
        case nodes.Assign(value=nodes.Const(value=bool())):
            return True
    return False

