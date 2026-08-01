
def get_layout_symints(node: ir.IRNode) -> OrderedSet[sympy.Symbol]:
    """Get free symbols from a node's layout (size, stride, offset)."""
    free_symbol_uses: OrderedSet[sympy.Symbol] = OrderedSet()
    layout = node.maybe_get_layout()
    if isinstance(layout, ir.Layout):
        free_symbol_uses.update(
            free_symbols(layout.size)
            | free_symbols(layout.stride)
            | free_symbols(layout.offset)
        )
        if isinstance(layout, ir.MutationLayoutSHOULDREMOVE):
            # symint may be used as index in layout.target
            free_symbol_uses.update(get_layout_symints(layout.target))
    else:
        assert layout is None, f"Expect layout to be None but found layout={layout}"
    return free_symbol_uses

