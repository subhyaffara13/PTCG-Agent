
def _looks_like_namespace(node) -> bool:
    func = node.func
    if isinstance(func, nodes.Attribute):
        return (
            func.attrname == "Namespace"
            and isinstance(func.expr, nodes.Name)
            and func.expr.name == "argparse"
        )
    return False

