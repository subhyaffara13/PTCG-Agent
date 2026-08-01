
def test_TSP_method():
    G = nx.cycle_graph(9)
    G[4][5]["weight"] = 10

    # Test using the old currying method
    def sa_tsp(G, weight):
        return nx_app.simulated_annealing_tsp(G, "greedy", weight, source=4, seed=1)

    path = nx_app.traveling_salesman_problem(
        G,
        method=sa_tsp,
        cycle=False,
    )
    assert path == [4, 3, 2, 1, 0, 8, 7, 6, 5]

