
def test_from_numpy_array_nodelist_multigraph(nodes):
    A = np.array(
        [
            [0, 1, 0, 0, 0],
            [1, 0, 2, 0, 0],
            [0, 2, 0, 3, 0],
            [0, 0, 3, 0, 4],
            [0, 0, 0, 4, 0],
        ]
    )

    H = nx.MultiGraph()
    for i, edge in enumerate(((0, 1), (1, 2), (2, 3), (3, 4))):
        H.add_edges_from(itertools.repeat(edge, i + 1))
    expected = nx.relabel_nodes(H, mapping=dict(enumerate(nodes)), copy=True)

    G = nx.from_numpy_array(
        A,
        parallel_edges=True,
        create_using=nx.MultiGraph,
        edge_attr=None,
        nodelist=nodes,
    )
    assert graphs_equal(G, expected)

