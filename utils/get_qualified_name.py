
def get_qualified_name(o: Expression) -> str:
    if isinstance(o, NameExpr):
        return o.name
    elif isinstance(o, MemberExpr):
        return f"{get_qualified_name(o.expr)}.{o.name}"
    else:
        return ERROR_MARKER


def get_qualified_name(func):
    return func.__qualname__

