
def read_fstring_item(state: State, data: ReadBuffer) -> Expression:
    t = read_tag(data)
    if t == LITERAL_STR:
        str_expr = StrExpr(read_str_bare(data))
        read_loc(data, str_expr)
        return str_expr
    elif t == nodes.FSTRING_INTERPOLATION:
        expr = read_expression(state, data)

        # Read conversion flag such as !r
        has_conv = read_bool(data)
        if has_conv:
            c = read_str(data)
            fmt = "{" + c + ":{}}"
        else:
            fmt = "{:{}}"

        # Read format spec such as <30 (which may have nested {...})
        has_spec = read_bool(data)
        if has_spec:
            spec = read_fstring_items(state, data)
        else:
            spec = StrExpr("")

        member = MemberExpr(StrExpr(fmt), "format")
        set_line_column(member, expr)
        call = CallExpr(member, [expr, spec], [ARG_POS, ARG_POS], [None, None])
        set_line_column(call, expr)
        expect_end_tag(data)
        return call
    else:
        raise ValueError(f"Unexpected tag {t}")

