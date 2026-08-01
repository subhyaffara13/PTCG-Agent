
def test_is_regular_expander(n):
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    G = nx.complete_graph(n)

    assert nx.is_regular_expander(G), "Should be a regular expander"

