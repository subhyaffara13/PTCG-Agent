
def names_modified_by_assignment(s: AssignmentStmt) -> list[NameExpr]:
    """Return all unqualified (short) names assigned to in an assignment statement."""
    result: list[NameExpr] = []
    for lvalue in s.lvalues:
        result += names_modified_in_lvalue(lvalue)
    return result

