
def local_names(node):
    names = set()
    if isinstance(node, ast.FunctionDef):
        names |= param_names(node)
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                names.add(item.name)
                names |= param_names(item)
            elif isinstance(item, ast.ClassDef):
                names.add(item.name)
    return names

