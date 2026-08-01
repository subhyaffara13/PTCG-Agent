
def test_bfs_layout_barbell():
    G = nx.barbell_graph(5, 3)
    # Start in one of the "bells"
    pos = nx.bfs_layout(G, start=0)
    # start, bell-1, [1] * len(bar)+1, bell-1
    expected_nodes_per_layer = [1, 4, 1, 1, 1, 1, 4]
    assert np.array_equal(_num_nodes_per_bfs_layer(pos), expected_nodes_per_layer)
    # Start in the other "bell" - expect same layer pattern
    pos = nx.bfs_layout(G, start=12)
    assert np.array_equal(_num_nodes_per_bfs_layer(pos), expected_nodes_per_layer)
    # Starting in the center of the bar, expect layers to be symmetric
    pos = nx.bfs_layout(G, start=6)
    # Expected layers: {6 (start)}, {5, 7}, {4, 8}, {8 nodes from remainder of bells}
    expected_nodes_per_layer = [1, 2, 2, 8]
    assert np.array_equal(_num_nodes_per_bfs_layer(pos), expected_nodes_per_layer)

