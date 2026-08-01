
def test_to_numpy_array_multigraph_nodelist(multigraph_test_graph):
    G = multigraph_test_graph
    G.add_edge(0, 1, weight=3)
    A = nx.to_numpy_array(G, nodelist=[1, 2])
    assert A.shape == (2, 2)
    assert A[1, 0] == 77

