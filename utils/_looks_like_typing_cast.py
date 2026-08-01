
def _looks_like_typing_cast(node: nodes.Call) -> bool:
    return (isinstance(node.func, nodes.Name) and node.func.name == "cast") or (
        isinstance(node.func, nodes.Attribute) and node.func.attrname == "cast"
    )

