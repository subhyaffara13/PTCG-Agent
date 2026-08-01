
def _is_from_future_import(stmt: nodes.ImportFrom, name: str) -> bool | None:
    """Check if the name is a future import from another module."""
    try:
        module = stmt.do_import_module(stmt.modname)
    except astroid.AstroidBuildingError:
        return None

    for local_node in module.locals.get(name, []):
        if isinstance(local_node, nodes.ImportFrom) and local_node.modname == FUTURE:
            return True
    return None

