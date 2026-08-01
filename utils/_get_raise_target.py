
def _get_raise_target(node: nodes.NodeNG) -> nodes.NodeNG | UninferableBase | None:
    match node.exc:
        case nodes.Call(func=nodes.Name() | nodes.Attribute() as func):
            return utils.safe_infer(func)
    return None

