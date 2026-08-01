
def names_modified_in_lvalue(lvalue: Lvalue) -> list[NameExpr]:
    """Return all NameExpr assignment targets in an Lvalue."""
    if isinstance(lvalue, NameExpr):
        return [lvalue]
    elif isinstance(lvalue, StarExpr):
        return names_modified_in_lvalue(lvalue.expr)
    elif isinstance(lvalue, (ListExpr, TupleExpr)):
        result: list[NameExpr] = []
        for item in lvalue.items:
            result += names_modified_in_lvalue(item)
        return result
    return []

