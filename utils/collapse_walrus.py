
def collapse_walrus(e: Expression) -> Expression:
    """If an expression is an AssignmentExpr, pull out the assignment target.

    We don't make any attempt to pull out all the targets in code like `x := (y := z)`.
    We could support narrowing those if that sort of code turns out to be common.
    """
    if isinstance(e, AssignmentExpr):
        return e.target
    return e

