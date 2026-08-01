
def _is_name_or_attr(node, name):  # type: (ast.AST, str) -> bool
    return (
        (isinstance(node, ast.Name) and node.id == name) or
        (isinstance(node, ast.Attribute) and node.attr == name)
    )

