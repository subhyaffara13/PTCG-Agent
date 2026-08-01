
def test_no_flow_satisfying_demands(simple_no_flow_graph):
    G = simple_no_flow_graph
    with pytest.raises(
        nx.NetworkXUnfeasible,
        match="no flow satisfies all node demands",
    ):
        nx.network_simplex(G)

