
def test_TSP_alternate_weight():
    G = nx.complete_graph(9)
    G[0][1]["weight"] = 2
    G[1][2]["weight"] = 2
    G[2][3]["weight"] = 2
    G[3][4]["weight"] = 4
    G[4][5]["weight"] = 5
    G[5][6]["weight"] = 4
    G[6][7]["weight"] = 2
    G[7][8]["weight"] = 2
    G[8][0]["weight"] = 2

    H = nx.complete_graph(9)
    H[0][1]["distance"] = 2
    H[1][2]["distance"] = 2
    H[2][3]["distance"] = 2
    H[3][4]["distance"] = 4
    H[4][5]["distance"] = 5
    H[5][6]["distance"] = 4
    H[6][7]["distance"] = 2
    H[7][8]["distance"] = 2
    H[8][0]["distance"] = 2

    assert nx_app.traveling_salesman_problem(
        G, weight="weight"
    ) == nx_app.traveling_salesman_problem(H, weight="distance")

