
def get_local_names(node):
    """Collect locally-defined names (params, nested defs) for a function or class."""
    names = set()
    if isinstance(node, ast.FunctionDef):
        names |= _func_param_names(node)
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                names.add(item.name)
                names |= _func_param_names(item)
            elif isinstance(item, ast.ClassDef):
                names.add(item.name)
    return names

