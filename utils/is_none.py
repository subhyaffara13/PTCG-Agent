
def is_none(node: nodes.NodeNG) -> bool:
    match node:
        case None | nodes.Const(value=None) | nodes.Name(value="None"):
            return True
    return False

