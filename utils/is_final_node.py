
def is_final_node(node: SymbolNode | None) -> bool:
    """Check whether `node` corresponds to a final attribute."""
    return isinstance(node, (Var, FuncDef, OverloadedFuncDef, Decorator)) and node.is_final

