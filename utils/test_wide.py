
def test_wide(width):
    """All nodes are searched when `width` is None or >= max degree"""
    G = nx.cycle_graph(4)
    edges = nx.bfs_beam_edges(G, source=0, value=lambda n: n, width=width)
    assert list(edges) == [(0, 3), (0, 1), (3, 2)]

