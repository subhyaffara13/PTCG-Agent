
def in_for_else_branch(parent: nodes.NodeNG, stmt: Statement) -> bool:
    """Returns True if stmt is inside the else branch for a parent For stmt."""
    return isinstance(parent, nodes.For) and any(
        else_stmt.parent_of(stmt) or else_stmt == stmt for else_stmt in parent.orelse
    )

