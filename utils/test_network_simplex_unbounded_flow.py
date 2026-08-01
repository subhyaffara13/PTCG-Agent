
def test_network_simplex_unbounded_flow():
    G = nx.DiGraph()
    # Add nodes
    G.add_node("A")
    G.add_node("B")
    G.add_node("C")

    # Add edges forming a negative cycle
    G.add_weighted_edges_from([("A", "B", -5), ("B", "C", -5), ("C", "A", -5)])

    with pytest.raises(
        nx.NetworkXUnbounded,
        match="negative cycle with infinite capacity found",
    ):
        nx.network_simplex(G)

