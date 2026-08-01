
def test_maybe_regular_expander_graph_max_tries():
    pytest.importorskip("numpy")
    d, n = 4, 10
    msg = "Too many iterations in maybe_regular_expander_graph"
    with pytest.raises(nx.NetworkXError, match=msg):
        nx.maybe_regular_expander_graph(n, d, max_tries=100, seed=6818)  # See gh-8048

    nx.maybe_regular_expander_graph(n, d, max_tries=130, seed=6818)

