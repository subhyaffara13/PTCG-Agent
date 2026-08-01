
def read_try_stmt(state: State, data: ReadBuffer) -> TryStmt:
    body = read_block(state, data)
    num_handlers = read_int(data)

    types_list: list[Expression | None] = []
    for _ in range(num_handlers):
        has_type = read_bool(data)
        if has_type:
            exc_type = read_expression(state, data)
            types_list.append(exc_type)
        else:
            types_list.append(None)

    vars_list: list[NameExpr | None] = []
    for _ in range(num_handlers):
        has_name = read_bool(data)
        if has_name:
            var_name = read_str(data)
            var_expr = NameExpr(var_name)
            read_loc(data, var_expr)
            vars_list.append(var_expr)
        else:
            vars_list.append(None)

    handlers = []
    for _ in range(num_handlers):
        handler_body = read_block(state, data)
        handlers.append(handler_body)

    has_else = read_bool(data)
    if has_else:
        else_body = read_block(state, data)
    else:
        else_body = None

    has_finally = read_bool(data)
    if has_finally:
        finally_body = read_block(state, data)
    else:
        finally_body = None

    # except* (Python 3.11+)
    is_star = read_bool(data)

    stmt = TryStmt(body, vars_list, types_list, handlers, else_body, finally_body)
    stmt.is_star = is_star
    read_loc(data, stmt)
    if is_star:
        state.check_min_version("Exception groups", (3, 11), stmt.line, stmt.column)
        if state.options.python_version < (3, 11):
            stmt.is_star = False
    expect_end_tag(data)
    return stmt

