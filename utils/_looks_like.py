
def _looks_like(node, name) -> bool:
    func = node.func
    if isinstance(func, nodes.Attribute):
        return func.attrname == name
    if isinstance(func, nodes.Name):
        return func.name == name
    return False

