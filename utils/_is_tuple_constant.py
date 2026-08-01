
def _is_tuple_constant(node):  # type: (ast.AST) -> bool
    return (
        isinstance(node, ast.Tuple) and
        all(_is_constant(elt) for elt in node.elts)
    )

