
def _names_from_node(node):
    if isinstance(node, ast.Import):
        for alias in node.names:
            yield alias.asname or alias.name.split('.')[0]
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            yield alias.asname or alias.name
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                yield target.id
            elif isinstance(target, (ast.List, ast.Tuple)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        yield elt.id
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.AugAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.Try):
        for child in node.body:
            yield from _names_from_node(child)
        for handler in node.handlers:
            for child in handler.body:
                yield from _names_from_node(child)
    elif isinstance(node, ast.If) and not _is_name_main_check(node):
        for child in node.body:
            yield from _names_from_node(child)

