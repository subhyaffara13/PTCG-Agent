
def test_nonzero_selfloop_with_single_edge_in_edgelist(subplots):
    """Ensure that selfloop extent is non-zero when only a single edge is
    specified in the edgelist.
    """
    # Create explicit axis object for test
    fig, ax = subplots
    # Graph with selfloop
    G = nx.path_graph(2, create_using=nx.DiGraph)
    G.add_edge(1, 1)
    pos = {n: (n, n) for n in G.nodes}
    # Draw only the selfloop edge via the `edgelist` kwarg
    patch = nx.draw_networkx_edges(G, pos, edgelist=[(1, 1)])[0]
    # The resulting patch must have non-zero extent
    bbox = patch.get_extents()
    assert bbox.width > 0 and bbox.height > 0

