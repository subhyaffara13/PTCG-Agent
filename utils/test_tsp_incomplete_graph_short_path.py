
def test_TSP_incomplete_graph_short_path():
    G = nx.cycle_graph(9)
    G.add_edges_from([(4, 9), (9, 10), (10, 11), (11, 0)])
    G[4][5]["weight"] = 5

    cycle = nx_app.traveling_salesman_problem(G)
    assert len(cycle) == 17 and len(set(cycle)) == 12

    # make sure that cutting one edge out of complete graph formulation
    # cuts out many edges out of the path of the TSP
    path = nx_app.traveling_salesman_problem(G, cycle=False)
    assert len(path) == 13 and len(set(path)) == 12

