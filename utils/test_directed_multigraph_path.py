
def test_directed_multigraph_path():
    G = nx.MultiDiGraph()
    nx.add_path(G, range(6))
    partition = [{0, 1}, {2, 3}, {4, 5}]
    M = nx.quotient_graph(G, partition, relabel=True)
    assert nodes_equal(M, [0, 1, 2])
    assert edges_equal(M.edges(), [(0, 1), (1, 2)], directed=True)
    for n in M:
        assert M.nodes[n]["nedges"] == 1
        assert M.nodes[n]["nnodes"] == 2
        assert M.nodes[n]["density"] == 0.5

