
def test_gh_8271(labels):
    """Test for graphs with nonstandard node labels."""
    pytest.importorskip("numpy")
    G = nx.complete_graph(labels)
    assert approx.densest_subgraph(G, method="fista") == (1, set(labels))

