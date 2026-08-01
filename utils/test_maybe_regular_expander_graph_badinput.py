
def test_maybe_regular_expander_graph_badinput():
    pytest.importorskip("numpy")

    with pytest.raises(nx.NetworkXError, match="n must be a positive integer"):
        nx.maybe_regular_expander_graph(n=-1, d=2)

    with pytest.raises(nx.NetworkXError, match="d must be greater than or equal to 2"):
        nx.maybe_regular_expander_graph(n=10, d=0)

    with pytest.raises(nx.NetworkXError, match="Need n-1>= d to have room"):
        nx.maybe_regular_expander_graph(n=5, d=6)

