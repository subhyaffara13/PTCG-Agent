
def strip_contents_from_if_stmt(stmt: IfStmt) -> None:
    """Remove contents from IfStmt.

    Needed to still be able to check the conditions after the contents
    have been merged with the surrounding function overloads.
    """
    if len(stmt.body) == 1:
        stmt.body[0].body = []
    if stmt.else_body and len(stmt.else_body.body) == 1:
        if isinstance(stmt.else_body.body[0], IfStmt):
            strip_contents_from_if_stmt(stmt.else_body.body[0])
        else:
            stmt.else_body.body = []

