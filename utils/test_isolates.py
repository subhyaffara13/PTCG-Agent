
def test_isolates():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_nodes_from([2, 3])
    assert sorted(nx.isolates(G)) == [2, 3]

