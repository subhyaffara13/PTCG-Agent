
def _extract_function_body_lines(source_lines, func_name):
    """Extract line numbers of a function's body."""
    source = ''.join(source_lines)
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node.lineno, node.end_lineno
    return None, None

