
def test_barbell_plus():
    G = nx.barbell_graph(3, 0)
    # Add an extra edge joining the bells.
    G.add_edge(0, 5)
    partition = [{0, 1, 2}, {3, 4, 5}]
    M = nx.quotient_graph(G, partition, relabel=True)
    assert nodes_equal(M, [0, 1])
    assert edges_equal(M.edges(), [(0, 1)])
    assert M[0][1]["weight"] == 2
    for n in M:
        assert M.nodes[n]["nedges"] == 3
        assert M.nodes[n]["nnodes"] == 3
        assert M.nodes[n]["density"] == 1

