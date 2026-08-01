
def test_digraph1():
    # From Bradley, S. P., Hax, A. C. and Magnanti, T. L. Applied
    # Mathematical Programming. Addison-Wesley, 1977.
    G = nx.DiGraph()
    G.add_node(1, demand=-20)
    G.add_node(4, demand=5)
    G.add_node(5, demand=15)
    G.add_edges_from(
        [
            (1, 2, {"capacity": 15, "weight": 4}),
            (1, 3, {"capacity": 8, "weight": 4}),
            (2, 3, {"weight": 2}),
            (2, 4, {"capacity": 4, "weight": 2}),
            (2, 5, {"capacity": 10, "weight": 6}),
            (3, 4, {"capacity": 15, "weight": 1}),
            (3, 5, {"capacity": 5, "weight": 3}),
            (4, 5, {"weight": 2}),
            (5, 3, {"capacity": 4, "weight": 1}),
        ]
    )
    flowCost, H = nx.network_simplex(G)
    soln = {
        1: {2: 12, 3: 8},
        2: {3: 8, 4: 4, 5: 0},
        3: {4: 11, 5: 5},
        4: {5: 10},
        5: {3: 0},
    }
    assert flowCost == 150
    assert nx.min_cost_flow_cost(G) == 150
    assert H == soln

