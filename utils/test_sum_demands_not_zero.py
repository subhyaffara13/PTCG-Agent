
def test_sum_demands_not_zero(simple_no_flow_graph):
    G = simple_no_flow_graph
    nx.set_node_attributes(G, {"t": {"demand": 4}})
    with pytest.raises(
        nx.NetworkXUnfeasible,
        match="total node demand is not zero",
    ):
        nx.network_simplex(G)

