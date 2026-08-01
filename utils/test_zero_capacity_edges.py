
def test_zero_capacity_edges():
    """Address issue raised in ticket #617 by arv."""
    G = nx.DiGraph()
    G.add_edges_from(
        [
            (1, 2, {"capacity": 1, "weight": 1}),
            (1, 5, {"capacity": 1, "weight": 1}),
            (2, 3, {"capacity": 0, "weight": 1}),
            (2, 5, {"capacity": 1, "weight": 1}),
            (5, 3, {"capacity": 2, "weight": 1}),
            (5, 4, {"capacity": 0, "weight": 1}),
            (3, 4, {"capacity": 2, "weight": 1}),
        ]
    )
    G.nodes[1]["demand"] = -1
    G.nodes[2]["demand"] = -1
    G.nodes[4]["demand"] = 2

    flowCost, H = nx.network_simplex(G)
    soln = {1: {2: 0, 5: 1}, 2: {3: 0, 5: 1}, 3: {4: 2}, 4: {}, 5: {3: 2, 4: 0}}
    assert flowCost == 6
    assert nx.min_cost_flow_cost(G) == 6
    assert H == soln

