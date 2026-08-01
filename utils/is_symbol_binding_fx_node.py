
def is_symbol_binding_fx_node(node: torch.fx.Node) -> sympy.Symbol | None:
    """
    Check if a given FX node is a symbol binding node.

    A symbol binding node is one that has a SymInt value in its meta that contains
    a sympy Symbol expression, and is either a placeholder node or contains unbacked symbols.

    Args:
        node (torch.fx.Node): The FX node to check

    Returns:
        Optional[sympy.Symbol]: The sympy Symbol if the node is a symbol binding node, None otherwise
    """
    if (
        "val" in node.meta
        and isinstance(node.meta["val"], torch.SymInt)
        and isinstance(node.meta["val"].node.expr, sympy.Symbol)
        and (
            node.op == "placeholder"
            or free_unbacked_symbols(node.meta["val"].node.expr)
        )
    ):
        return node.meta["val"].node.expr
    return None

