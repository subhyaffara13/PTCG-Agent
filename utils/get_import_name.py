
def get_import_name(importnode: ImportNode, modname: str | None) -> str | None:
    """Get a prepared module name from the given import node.

    In the case of relative imports, this will return the
    absolute qualified module name, which might be useful
    for debugging. Otherwise, the initial module name
    is returned unchanged.

    :param importnode: node representing import statement.
    :param modname: module name from import statement.
    :returns: absolute qualified module name of the module
        used in import.
    """
    if isinstance(importnode, nodes.ImportFrom) and importnode.level:
        root = importnode.root()
        if isinstance(root, nodes.Module):
            try:
                return root.relative_to_absolute_name(  # type: ignore[no-any-return]
                    modname, level=importnode.level
                )
            except TooManyLevelsError:
                return modname
    return modname

