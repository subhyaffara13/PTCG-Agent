
def _import_name_is_global(
    stmt: nodes.Global | _base_nodes.ImportNode,
    global_names: set[str],
) -> bool:
    for import_name, import_alias in stmt.names:
        # If the import uses an alias, check only that.
        # Otherwise, check only the import name.
        if import_alias:
            if import_alias in global_names:
                return True
        elif import_name in global_names:
            return True
    return False

