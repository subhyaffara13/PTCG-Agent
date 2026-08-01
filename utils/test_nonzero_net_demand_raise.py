
def test_nonzero_net_demand_raise(simple_flow_graph):
    G = simple_flow_graph
    nx.set_node_attributes(G, {"b": {"demand": -4}})
    with pytest.raises(
        nx.NetworkXUnfeasible,
        match="total node demand is not zero",
    ):
        nx.network_simplex(G)

