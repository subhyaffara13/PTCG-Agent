
def build_fstring_join(data: ReadBuffer, items: list[Expression]) -> Expression:
    items = collapse_consecutive_str_items(items)
    if len(items) == 1:
        expr = items[0]
        read_loc(data, expr)
        return expr
    args = ListExpr(items)
    str_expr = StrExpr("")
    member = MemberExpr(str_expr, "join")
    call = CallExpr(member, [args], [ARG_POS], [None])
    read_loc(data, call)
    set_line_column(args, call)
    set_line_column(str_expr, call)
    set_line_column(member, call)
    return call

