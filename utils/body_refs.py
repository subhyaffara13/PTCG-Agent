
def body_refs(source, func_names):
    tree = ast.parse(source)
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in func_names:
            local = local_names(node)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id not in BUILTINS and sub.id not in local:
                    refs.add(sub.id)
    return refs

