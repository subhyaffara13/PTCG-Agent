
def _parse_assignments(
    lvalue: Expression, stmt: AssignmentStmt
) -> tuple[list[NameExpr], list[Expression]]:
    """Convert a possibly complex assignment expression into lists of lvalues and rvalues."""
    lvalues: list[NameExpr] = []
    rvalues: list[Expression] = []
    if isinstance(lvalue, (TupleExpr, ListExpr)):
        if all(isinstance(item, NameExpr) for item in lvalue.items):
            lvalues = cast(list[NameExpr], lvalue.items)
        if isinstance(stmt.rvalue, (TupleExpr, ListExpr)):
            rvalues = stmt.rvalue.items
    elif isinstance(lvalue, NameExpr):
        lvalues = [lvalue]
        rvalues = [stmt.rvalue]
    return lvalues, rvalues

