
def is_true_literal(n: Expression) -> bool:
    """Returns true if this expression is the 'True' literal/keyword."""
    return refers_to_fullname(n, "builtins.True") or isinstance(n, IntExpr) and n.value != 0

