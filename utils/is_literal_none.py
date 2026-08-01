
def is_literal_none(n: Expression) -> bool:
    """Returns true if this expression is the 'None' literal/keyword."""
    return isinstance(n, NameExpr) and n.fullname == "builtins.None"

