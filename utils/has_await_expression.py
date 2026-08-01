
def has_await_expression(expr: Expression) -> bool:
    seeker = AwaitSeeker()
    expr.accept(seeker)
    return seeker.found

