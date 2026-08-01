
def test_attr_sparse_matrix():
    pytest.importorskip("scipy")
    G = nx.Graph()
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 2, thickness=2)
    G.add_edge(1, 2, thickness=3)
    M = nx.attr_sparse_matrix(G)
    mtx = M[0]
    data = np.ones((3, 3), float)
    np.fill_diagonal(data, 0)
    np.testing.assert_equal(mtx.todense(), np.array(data))
    assert M[1] == [0, 1, 2]

