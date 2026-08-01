
def _is_singleton(node):  # type: (ast.AST) -> bool
    return (
        isinstance(node, ast.Constant) and
        isinstance(node.value, (bool, type(Ellipsis), type(None)))
    )

