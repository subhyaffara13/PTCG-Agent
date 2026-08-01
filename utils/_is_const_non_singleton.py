
def _is_const_non_singleton(node):  # type: (ast.AST) -> bool
    return _is_constant(node) and not _is_singleton(node)

