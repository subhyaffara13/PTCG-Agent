
def is_classmethod_node(node: SymbolNode | None) -> bool | None:
    """Find out if a node describes a classmethod."""
    if isinstance(node, Decorator):
        node = node.func
    if isinstance(node, FuncDef):
        return node.is_class
    if isinstance(node, Var):
        return node.is_classmethod
    return None

