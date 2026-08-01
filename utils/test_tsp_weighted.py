
def test_TSP_weighted():
    G = nx.cycle_graph(9)
    G[0][1]["weight"] = 2
    G[1][2]["weight"] = 2
    G[2][3]["weight"] = 2
    G[3][4]["weight"] = 4
    G[4][5]["weight"] = 5
    G[5][6]["weight"] = 4
    G[6][7]["weight"] = 2
    G[7][8]["weight"] = 2
    G[8][0]["weight"] = 2
    tsp = nx_app.traveling_salesman_problem

    # path between 3 and 6
    expected_paths = ([3, 2, 1, 0, 8, 7, 6], [6, 7, 8, 0, 1, 2, 3])
    # cycle between 3 and 6
    expected_cycles = (
        [3, 2, 1, 0, 8, 7, 6, 7, 8, 0, 1, 2, 3],
        [6, 7, 8, 0, 1, 2, 3, 2, 1, 0, 8, 7, 6],
    )
    # path through all nodes
    expected_tourpaths = ([5, 6, 7, 8, 0, 1, 2, 3, 4], [4, 3, 2, 1, 0, 8, 7, 6, 5])

    # Check default method
    cycle = tsp(G, nodes=[3, 6], weight="weight")
    assert cycle in expected_cycles

    path = tsp(G, nodes=[3, 6], weight="weight", cycle=False)
    assert path in expected_paths

    tourpath = tsp(G, weight="weight", cycle=False)
    assert tourpath in expected_tourpaths

    # Check all methods
    methods = [
        (nx_app.christofides, {}),
        (nx_app.greedy_tsp, {}),
        (
            nx_app.simulated_annealing_tsp,
            {"init_cycle": "greedy"},
        ),
        (
            nx_app.threshold_accepting_tsp,
            {"init_cycle": "greedy"},
        ),
    ]
    for method, kwargs in methods:
        cycle = tsp(G, nodes=[3, 6], weight="weight", method=method, **kwargs)
        assert cycle in expected_cycles

        path = tsp(
            G, nodes=[3, 6], weight="weight", method=method, cycle=False, **kwargs
        )
        assert path in expected_paths

        tourpath = tsp(G, weight="weight", method=method, cycle=False, **kwargs)
        assert tourpath in expected_tourpaths

