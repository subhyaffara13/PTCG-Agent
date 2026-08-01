
def names_from_node(node):
    if isinstance(node, ast.Import):
        for a in node.names:
            yield a.asname or a.name.split('.')[0]
    elif isinstance(node, ast.ImportFrom):
        for a in node.names:
            yield a.asname or a.name
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                yield t.id
            elif isinstance(t, (ast.List, ast.Tuple)):
                for elt in t.elts:
                    if isinstance(elt, ast.Name):
                        yield elt.id
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.Try):
        for c in node.body:
            yield from names_from_node(c)
        for h in node.handlers:
            for c in h.body:
                yield from names_from_node(c)
    elif isinstance(node, ast.If):
        for c in node.body:
            yield from names_from_node(c)

