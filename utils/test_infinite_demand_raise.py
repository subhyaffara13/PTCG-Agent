
def test_infinite_demand_raise(simple_flow_graph):
    G = simple_flow_graph
    inf = float("inf")
    node_name = "a"
    nx.set_node_attributes(G, {node_name: {"demand": inf}})
    with pytest.raises(
        nx.NetworkXError,
        match=f"node '{node_name}' has infinite demand",
    ):
        nx.network_simplex(G)

