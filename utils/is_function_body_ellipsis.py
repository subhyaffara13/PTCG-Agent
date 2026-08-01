
def is_function_body_ellipsis(node: nodes.FunctionDef) -> bool:
    """Checks whether a function body only consists of a single Ellipsis."""
    match node.body:
        case [nodes.Expr(value=nodes.Const(value=value))]:
            return value is Ellipsis
    return False

