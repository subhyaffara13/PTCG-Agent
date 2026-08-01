
def get_body_refs_for_funcs(source, func_names):
    tree = ast.parse(source)
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in func_names:
            local_names = get_local_names(node)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id not in BUILTIN_NAMES and sub.id not in local_names:
                    refs.add(sub.id)
    return refs

