
def test_long_paths_graphs():
    """Smoke test for potential RecursionError. See gh-7945."""
    G = nx.path_graph(10_000)
    nx.isomorphism.rooted_tree_isomorphism(G, 0, G, 0) == [(n, n) for n in G]

