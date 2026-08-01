
def is_trivial_body(block: Block) -> bool:
    """Returns 'true' if the given body is "trivial" -- if it contains just a "pass",
    "..." (ellipsis), or "raise NotImplementedError()". A trivial body may also
    start with a statement containing just a string (e.g. a docstring).

    Note: Functions that raise other kinds of exceptions do not count as
    "trivial". We use this function to help us determine when it's ok to
    relax certain checks on body, but functions that raise arbitrary exceptions
    are more likely to do non-trivial work. For example:

       def halt(self, reason: str = ...) -> NoReturn:
           raise MyCustomError("Fatal error: " + reason, self.line, self.context)

    A function that raises just NotImplementedError is much less likely to be
    this complex.

    Note: If you update this, you may also need to update
    mypy.fastparse.is_possible_trivial_body!
    """
    body = block.body
    if not body:
        # Functions have empty bodies only if the body is stripped or the function is
        # generated or deserialized. In these cases the body is unknown.
        return False

    # Skip a docstring
    if isinstance(body[0], ExpressionStmt) and isinstance(body[0].expr, StrExpr):
        body = block.body[1:]

    if len(body) == 0:
        # There's only a docstring (or no body at all).
        return True
    elif len(body) > 1:
        return False

    stmt = body[0]

    if isinstance(stmt, RaiseStmt):
        expr = stmt.expr
        if expr is None:
            return False
        if isinstance(expr, CallExpr):
            expr = expr.callee

        return isinstance(expr, NameExpr) and expr.fullname == "builtins.NotImplementedError"

    return isinstance(stmt, PassStmt) or (
        isinstance(stmt, ExpressionStmt) and isinstance(stmt.expr, EllipsisExpr)
    )

