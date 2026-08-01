
def test_modularity():
    G = nx.barbell_graph(3, 0)
    C = [{0, 1, 4}, {2, 3, 5}]
    assert (-16 / (14**2)) == pytest.approx(modularity(G, C), abs=1e-7)
    C = [{0, 1, 2}, {3, 4, 5}]
    assert (35 * 2) / (14**2) == pytest.approx(modularity(G, C), abs=1e-7)

    n = 1000
    G = nx.erdos_renyi_graph(n, 0.09, seed=42, directed=True)
    C = [set(range(n // 2)), set(range(n // 2, n))]
    assert 0.00017154251389292754 == pytest.approx(modularity(G, C), abs=1e-7)

    G = nx.margulis_gabber_galil_graph(10)
    mid_value = G.number_of_nodes() // 2
    nodes = list(G.nodes)
    C = [set(nodes[:mid_value]), set(nodes[mid_value:])]
    assert 0.13 == pytest.approx(modularity(G, C), abs=1e-7)

    G = nx.DiGraph()
    G.add_edges_from([(2, 1), (2, 3), (3, 4)])
    C = [{1, 2}, {3, 4}]
    assert 2 / 9 == pytest.approx(modularity(G, C), abs=1e-7)

