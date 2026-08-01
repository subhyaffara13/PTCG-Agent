
def _class_methods(source, class_name):
    """Get all method names of a class."""
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
    return []

