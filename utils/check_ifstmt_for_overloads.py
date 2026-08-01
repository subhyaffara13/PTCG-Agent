
def check_ifstmt_for_overloads(
    stmt: IfStmt, current_overload_name: str | None = None
) -> str | None:
    """Check if IfStmt contains only overloads with the same name.
    Return overload_name if found, None otherwise.
    """
    # Check that block only contains a single Decorator, FuncDef, or OverloadedFuncDef.
    # Multiple overloads have already been merged as OverloadedFuncDef.
    if not (
        len(stmt.body[0].body) == 1
        and (
            isinstance(stmt.body[0].body[0], (Decorator, OverloadedFuncDef))
            or current_overload_name is not None
            and isinstance(stmt.body[0].body[0], FuncDef)
        )
        or len(stmt.body[0].body) > 1
        and isinstance(stmt.body[0].body[-1], OverloadedFuncDef)
        and all(is_stripped_if_stmt(if_stmt) for if_stmt in stmt.body[0].body[:-1])
    ):
        return None

    overload_name = cast(Decorator | FuncDef | OverloadedFuncDef, stmt.body[0].body[-1]).name
    if stmt.else_body is None or stmt.else_body.is_unreachable:
        return overload_name

    if len(stmt.else_body.body) == 1:
        # For elif: else_body contains an IfStmt itself -> do a recursive check.
        if (
            isinstance(stmt.else_body.body[0], (Decorator, FuncDef, OverloadedFuncDef))
            and stmt.else_body.body[0].name == overload_name
        ):
            return overload_name
        if (
            isinstance(stmt.else_body.body[0], IfStmt)
            and check_ifstmt_for_overloads(stmt.else_body.body[0], current_overload_name)
            == overload_name
        ):
            return overload_name

    return None

