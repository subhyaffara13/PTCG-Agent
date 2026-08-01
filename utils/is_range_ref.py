
def is_range_ref(expr: RefExpr) -> bool:
    return (
        expr.fullname == "builtins.range"
        or isinstance(expr.node, TypeAlias)
        and expr.fullname == "six.moves.xrange"
    )

