
def _top_level_names(source):
    """Get all top-level defined names (functions/classes)."""
    tree = ast.parse(source)
    names = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.append(node.name)
    return names

