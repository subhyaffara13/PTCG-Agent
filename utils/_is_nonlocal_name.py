
def _is_nonlocal_name(node: nodes.Name, frame: nodes.LocalsDictNodeNG) -> bool:
    """Checks if name node has a nonlocal declaration in the given frame."""
    if not isinstance(frame, nodes.FunctionDef):
        return False

    return any(
        isinstance(stmt, nodes.Nonlocal)
        and node.name in stmt.names
        and _is_before(stmt, node)
        for stmt in frame.body
    )

