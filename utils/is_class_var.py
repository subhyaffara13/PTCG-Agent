
def is_class_var(expr: NameExpr) -> bool:
    """Return whether the expression is ClassVar[...]"""
    if isinstance(expr.node, Var):
        return expr.node.is_classvar
    return False


def is_class_var(node: NodeNG) -> bool:
    """Return True if node is a ClassVar, with or without subscripting."""
    try:
        inferred = next(node.infer())
    except (InferenceError, StopIteration):
        return False

    return getattr(inferred, "name", "") == "ClassVar"

