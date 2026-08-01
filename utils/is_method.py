
def is_method(node: SymbolNode | None) -> bool:
    if isinstance(node, OverloadedFuncDef):
        return not node.is_property
    if isinstance(node, Decorator):
        return not node.var.is_property
    return isinstance(node, FuncDef)

