
def try_getting_str_literals(expr: Expression, typ: Type) -> list[str] | None:
    """If the given expression or type corresponds to a string literal
    or a union of string literals, returns a list of the underlying strings.
    Otherwise, returns None.

    Specifically, this function is guaranteed to return a list with
    one or more strings if one of the following is true:

    1. 'expr' is a StrExpr
    2. 'typ' is a LiteralType containing a string
    3. 'typ' is a UnionType containing only LiteralType of strings
    """
    if isinstance(expr, StrExpr):
        return [expr.value]

    # TODO: See if we can eliminate this function and call the below one directly
    return try_getting_str_literals_from_type(typ)

