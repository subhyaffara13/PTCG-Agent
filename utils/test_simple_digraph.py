
def test_simple_digraph():
    G = nx.DiGraph()
    G.add_node("a", demand=-5)
    G.add_node("d", demand=5)
    G.add_edge("a", "b", weight=3, capacity=4)
    G.add_edge("a", "c", weight=6, capacity=10)
    G.add_edge("b", "d", weight=1, capacity=9)
    G.add_edge("c", "d", weight=2, capacity=5)
    flowCost, H = nx.network_simplex(G)
    soln = {"a": {"b": 4, "c": 1}, "b": {"d": 4}, "c": {"d": 1}, "d": {}}
    assert flowCost == 24
    assert nx.min_cost_flow_cost(G) == 24
    assert H == soln

