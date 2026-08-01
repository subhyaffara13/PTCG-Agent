
def _looks_like_require_version(node) -> bool:
    # Return whether this looks like a call to gi.require_version(<name>, <version>)
    # Only accept function calls with two constant arguments
    if len(node.args) != 2:
        return False

    if not all(isinstance(arg, nodes.Const) for arg in node.args):
        return False

    func = node.func
    if isinstance(func, nodes.Attribute):
        if func.attrname != "require_version":
            return False
        if isinstance(func.expr, nodes.Name) and func.expr.name == "gi":
            return True

        return False

    if isinstance(func, nodes.Name):
        return func.name == "require_version"

    return False

