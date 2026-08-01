
def split_large_def(fp, source, lines, tree):
    """
    For a file with a single large function/class (>50 lines):
        Extract body parts into _helper files.
    """
    defs = [n for n in ast.iter_child_nodes(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]

    if not defs:
        return False

    big = [n for n in defs if (n.end_lineno - n.lineno) > TARGET]
    if not big:
        return False

    node = big[0]
    shared = [n for n in ast.iter_child_nodes(tree) if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]

    if isinstance(node, ast.ClassDef):
        return _split_class(fp, source, lines, node, shared)
    elif isinstance(node, ast.FunctionDef):
        return _split_function(fp, source, lines, node, shared)

    return False

