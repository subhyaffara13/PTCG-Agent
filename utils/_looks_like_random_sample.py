
def _looks_like_random_sample(node) -> bool:
    func = node.func
    if isinstance(func, nodes.Attribute):
        return func.attrname == "sample"
    if isinstance(func, nodes.Name):
        return func.name == "sample"
    return False

