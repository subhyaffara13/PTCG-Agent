
def _wildcard_import_binds(stmt: nodes.ImportFrom, name: str) -> bool:
    """Check if the name is exported by a `from X import *` statement."""
    if not any(node_name[0] == "*" for node_name in stmt.names):
        return False
    try:
        return name in stmt.do_import_module(stmt.modname).wildcard_import_names()
    except astroid.AstroidBuildingError:
        return False

