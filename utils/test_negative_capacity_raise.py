
def test_negative_capacity_raise(simple_flow_graph):
    G = simple_flow_graph
    nx.set_edge_attributes(G, {("a", "b"): {"weight": 1}, ("b", "d"): {"capacity": -9}})
    with pytest.raises(
        nx.NetworkXUnfeasible,
        match=r"edge .* has negative capacity",
    ):
        nx.network_simplex(G)

