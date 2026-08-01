
def test_attr_sparse_matrix_directed():
    pytest.importorskip("scipy")
    G = nx.DiGraph()
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 2, thickness=2)
    G.add_edge(1, 2, thickness=3)
    M = nx.attr_sparse_matrix(G, rc_order=[0, 1, 2])
    # fmt: off
    data = np.array(
        [[0., 1., 1.],
         [0., 0., 1.],
         [0., 0., 0.]]
    )
    # fmt: on
    np.testing.assert_equal(M.todense(), np.array(data))

