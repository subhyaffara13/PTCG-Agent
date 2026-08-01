
def get_member_expr_fullname(expr: MemberExpr) -> str | None:
    """Return the qualified name representation of a member expression.

    Return a string of form foo.bar, foo.bar.baz, or similar, or None if the
    argument cannot be represented in this form.
    """
    initial: str | None = None
    if isinstance(expr.expr, NameExpr):
        initial = expr.expr.name
    elif isinstance(expr.expr, MemberExpr):
        initial = get_member_expr_fullname(expr.expr)
    if initial is None:
        return None
    return f"{initial}.{expr.name}"

