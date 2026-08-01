
def test_attr_matrix_multigraph():
    G = nx.MultiGraph()
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 1, thickness=1, weight=3)
    G.add_edge(0, 2, thickness=2)
    G.add_edge(1, 2, thickness=3)
    M = nx.attr_matrix(G, rc_order=[0, 1, 2])
    # fmt: off
    data = np.array(
        [[0., 3., 1.],
         [3., 0., 1.],
         [1., 1., 0.]]
    )
    # fmt: on
    np.testing.assert_equal(M, np.array(data))
    M = nx.attr_matrix(G, edge_attr="weight", rc_order=[0, 1, 2])
    # fmt: off
    data = np.array(
        [[0., 9., 1.],
         [9., 0., 1.],
         [1., 1., 0.]]
    )
    # fmt: on
    np.testing.assert_equal(M, np.array(data))
    M = nx.attr_matrix(G, edge_attr="thickness", rc_order=[0, 1, 2])
    # fmt: off
    data = np.array(
        [[0., 3., 2.],
         [3., 0., 3.],
         [2., 3., 0.]]
    )
    # fmt: on
    np.testing.assert_equal(M, np.array(data))

