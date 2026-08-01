
def test_path():
    G = nx.DiGraph()
    nx.add_path(G, range(5))
    assert nx.is_branching(G)
    assert nx.is_arborescence(G)


def test_path():
    G = nx.path_graph(6)
    partition = [{0, 1}, {2, 3}, {4, 5}]
    M = nx.quotient_graph(G, partition, relabel=True)
    assert nodes_equal(M, [0, 1, 2])
    assert edges_equal(M.edges(), [(0, 1), (1, 2)])
    for n in M:
        assert M.nodes[n]["nedges"] == 1
        assert M.nodes[n]["nnodes"] == 2
        assert M.nodes[n]["density"] == 1

