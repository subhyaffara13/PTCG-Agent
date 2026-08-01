
def get_assigned_names(lvalues: Iterable[Expression]) -> Iterator[str]:
    for lvalue in lvalues:
        if isinstance(lvalue, NameExpr):
            yield lvalue.name
        elif isinstance(lvalue, TupleExpr):
            yield from get_assigned_names(lvalue.items)

