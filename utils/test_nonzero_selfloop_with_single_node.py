
def test_nonzero_selfloop_with_single_node(subplots):
    """Ensure that selfloop extent is non-zero when there is only one node."""
    # Create explicit axis object for test
    fig, ax = subplots
    # Graph with single node + self loop
    G = nx.DiGraph()
    G.add_node(0)
    G.add_edge(0, 0)
    # Draw
    patch = nx.draw_networkx_edges(G, {0: (0, 0)})[0]
    # The resulting patch must have non-zero extent
    bbox = patch.get_extents()
    assert bbox.width > 0 and bbox.height > 0

