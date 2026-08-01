
def is_possible_trivial_body(s: list[Statement]) -> bool:
    """Could the statements form a "trivial" function body, such as 'pass'?

    This mimics mypy.semanal.is_trivial_body, but this runs before
    semantic analysis so some checks must be conservative.
    """
    l = len(s)
    if l == 0:
        return False
    i = 0
    if isinstance(s[0], ExpressionStmt) and isinstance(s[0].expr, StrExpr):
        # Skip docstring
        i += 1
    if i == l:
        return True
    if l > i + 1:
        return False
    stmt = s[i]
    return isinstance(stmt, (PassStmt, RaiseStmt)) or (
        isinstance(stmt, ExpressionStmt) and isinstance(stmt.expr, EllipsisExpr)
    )

