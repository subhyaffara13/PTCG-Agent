
def set_info(node: SymbolNode, info: TypeInfo) -> None:
    """Add `info` attribute to all relevant components of the node."""
    if isinstance(node, (FuncDef, Var)):
        node.info = info
    elif isinstance(node, Decorator):
        node.var.info = info
        node.func.info = info
    elif isinstance(node, OverloadedFuncDef):
        node.info = info
        for item in node.items:
            set_info(item, info)
        if node.impl:
            set_info(node.impl, info)

