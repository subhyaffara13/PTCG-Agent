
def is_call_of_name(node: nodes.NodeNG, name: str) -> bool:
    """Checks if node is a function call with the given name."""
    match node:
        case nodes.Call(func=nodes.Name(name=func_name)):
            return func_name == name  # type: ignore[no-any-return]
    return False

