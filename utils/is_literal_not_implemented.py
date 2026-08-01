
def is_literal_not_implemented(n: Expression | None) -> bool:
    return isinstance(n, NameExpr) and n.fullname == "builtins.NotImplemented"

