
def is_stripped_if_stmt(stmt: Statement) -> bool:
    """Check stmt to make sure it is a stripped IfStmt.

    See also: strip_contents_from_if_stmt
    """
    if not isinstance(stmt, IfStmt):
        return False

    if not (len(stmt.body) == 1 and len(stmt.body[0].body) == 0):
        # Body not empty
        return False

    if not stmt.else_body or len(stmt.else_body.body) == 0:
        # No or empty else_body
        return True

    # For elif, IfStmt are stored recursively in else_body
    return is_stripped_if_stmt(stmt.else_body.body[0])

