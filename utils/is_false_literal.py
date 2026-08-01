
def is_false_literal(n: Expression) -> bool:
    """Returns true if this expression is the 'False' literal/keyword."""
    return refers_to_fullname(n, "builtins.False") or isinstance(n, IntExpr) and n.value == 0

