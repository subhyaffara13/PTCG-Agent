
def get_call_name(node, aliases):
    if isinstance(node.func, ast.Name):
        if deepgetattr(node, "func.id") in aliases:
            return aliases[deepgetattr(node, "func.id")]
        return deepgetattr(node, "func.id")
    elif isinstance(node.func, ast.Attribute):
        return _get_attr_qual_name(node.func, aliases)
    else:
        return ""

