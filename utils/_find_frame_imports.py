
def _find_frame_imports(name: str, frame: nodes.LocalsDictNodeNG) -> bool:
    """Detect imports in the frame, with the required *name*.

    Such imports can be considered assignments if they are not globals.
    Returns True if an import for the given name was found.
    """
    if name in _flattened_scope_names(frame.nodes_of_class(nodes.Global)):
        return False

    imports = frame.nodes_of_class((nodes.Import, nodes.ImportFrom))
    for import_node in imports:
        for import_name, import_alias in import_node.names:
            # If the import uses an alias, check only that.
            # Otherwise, check only the import name.
            if import_alias:
                if import_alias == name:
                    return True
            elif import_name and import_name == name:
                return True
    return False

