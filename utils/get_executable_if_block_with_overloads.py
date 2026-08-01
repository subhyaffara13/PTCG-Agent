
def get_executable_if_block_with_overloads(
    stmt: IfStmt, options: Options
) -> tuple[Block | None, IfStmt | None]:
    """Return block from IfStmt that will get executed.

    Return
        0 -> A block if sure that alternative blocks are unreachable.
        1 -> An IfStmt if the reachability of it can't be inferred,
             i.e. the truth value is unknown.
    """
    infer_reachability_of_if_statement(stmt, options)
    if stmt.else_body is None and stmt.body[0].is_unreachable is True:
        # always False condition with no else
        return None, None
    if (
        stmt.else_body is None
        or stmt.body[0].is_unreachable is False
        and stmt.else_body.is_unreachable is False
    ):
        # The truth value is unknown, thus not conclusive
        return None, stmt
    if stmt.else_body.is_unreachable:
        # else_body will be set unreachable if condition is always True
        return stmt.body[0], None
    if stmt.body[0].is_unreachable is True:
        # body will be set unreachable if condition is always False
        # else_body can contain an IfStmt itself (for elif) -> do a recursive check
        if isinstance(stmt.else_body.body[0], IfStmt):
            return get_executable_if_block_with_overloads(stmt.else_body.body[0], options)
        return stmt.else_body, None
    return None, stmt

