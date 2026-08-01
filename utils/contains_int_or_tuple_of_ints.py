
def contains_int_or_tuple_of_ints(expr: Expression) -> None | int | tuple[int, ...]:
    if isinstance(expr, IntExpr):
        return expr.value
    if isinstance(expr, TupleExpr):
        if literal(expr) == LITERAL_YES:
            thing = []
            for x in expr.items:
                if not isinstance(x, IntExpr):
                    return None
                thing.append(x.value)
            return tuple(thing)
    return None

