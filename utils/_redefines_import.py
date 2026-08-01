
def _redefines_import(node: nodes.AssignName) -> bool:
    """Detect that the given node (AssignName) is inside an
    exception handler and redefines an import from the tryexcept body.

    Returns True if the node redefines an import, False otherwise.
    """
    current = node
    while current and not isinstance(current.parent, nodes.ExceptHandler):
        current = current.parent
    if not (current and utils.error_of_type(current.parent, ImportError)):
        return False
    try_block = current.parent.parent
    for import_node in try_block.nodes_of_class((nodes.ImportFrom, nodes.Import)):
        for name, alias in import_node.names:
            if alias:
                if alias == node.name:
                    return True
            elif name == node.name:
                return True
    return False

