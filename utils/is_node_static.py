
def is_node_static(node: SymbolNode | None) -> bool | None:
    """Find out if a node describes a static function method."""
    if isinstance(node, Decorator):
        node = node.func
    if isinstance(node, FuncDef):
        return node.is_static
    if isinstance(node, Var):
        return node.is_staticmethod
    return None

