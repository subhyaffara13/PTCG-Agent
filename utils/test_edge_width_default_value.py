
def test_edge_width_default_value(graph_type):
    """Test the default linewidth for edges drawn either via LineCollection or
    FancyArrowPatches."""
    G = nx.path_graph(2, create_using=graph_type)
    pos = {n: (n, n) for n in range(len(G))}
    drawn_edges = nx.draw_networkx_edges(G, pos)
    if isinstance(drawn_edges, list):  # directed case: list of FancyArrowPatch
        drawn_edges = drawn_edges[0]
    assert drawn_edges.get_linewidth() == 1

