
def _free_non_source_unbacked_symbols(
    x: IterateExprs, unbacked_inputs: OrderedSet[sympy.Symbol]
) -> OrderedSet[sympy.Symbol]:
    """Unbacked symbols that are not inputs to the graph. These are symbols that originated from
    data-dependent operations as opposed to mark_unbacked calls."""
    unbacked_symbols = free_unbacked_symbols(x)
    non_source_symbols = unbacked_symbols - unbacked_inputs
    return non_source_symbols

