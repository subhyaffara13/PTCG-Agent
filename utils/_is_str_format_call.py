
def _is_str_format_call(node: nodes.Call) -> bool:
    """Catch calls to str.format()."""
    if not (isinstance(node.func, nodes.Attribute) and node.func.attrname == "format"):
        return False

    if isinstance(node.func.expr, nodes.Name):
        value = util.safe_infer(node.func.expr)
    else:
        value = node.func.expr

    return isinstance(value, nodes.Const) and isinstance(value.value, str)

