
def test_infinite_weight_raise(simple_flow_graph):
    G = simple_flow_graph
    inf = float("inf")
    nx.set_edge_attributes(
        G, {("a", "b"): {"weight": inf}, ("b", "d"): {"weight": inf}}
    )
    with pytest.raises(
        nx.NetworkXError,
        match=r"edge .* has infinite weight",
    ):
        nx.network_simplex(G)

