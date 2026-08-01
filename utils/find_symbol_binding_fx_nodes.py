
def find_symbol_binding_fx_nodes(
    graph: torch.fx.Graph,
) -> dict[sympy.Symbol, torch.fx.Node]:
    """
    Find all nodes in an FX graph that bind sympy Symbols.

    This function scans through all nodes in the given FX graph and identifies
    nodes that bind sympy Symbols (typically placeholder nodes with SymInt values).
    When multiple nodes bind the same symbol, only the first occurrence is kept.

    Args:
        graph: The FX graph to search for symbol binding nodes

    Returns:
        A dictionary mapping from sympy Symbols to their binding FX nodes
    """
    r: dict[sympy.Symbol, torch.fx.Node] = {}
    # NB: Prefer first occurrence of symbol
    for node in graph.nodes:
        if (s := is_symbol_binding_fx_node(node)) is not None and s not in r:
            r[s] = node
    return r

