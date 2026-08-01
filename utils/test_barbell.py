
def test_barbell():
    G = nx.barbell_graph(3, 0)
    partition = [{0, 1, 2}, {3, 4, 5}]
    M = nx.quotient_graph(G, partition, relabel=True)
    assert nodes_equal(M, [0, 1])
    assert edges_equal(M.edges(), [(0, 1)])
    for n in M:
        assert M.nodes[n]["nedges"] == 3
        assert M.nodes[n]["nnodes"] == 3
        assert M.nodes[n]["density"] == 1


def test_barbell():
    G = nx.barbell_graph(5, 0)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 2)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 3)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 4)
    _check_augmentations(G)


def test_barbell():
    G = nx.barbell_graph(8, 4)
    nx.add_path(G, [7, 20, 21, 22])
    nx.add_cycle(G, [22, 23, 24, 25])
    pts = set(nx.articulation_points(G))
    assert pts == {7, 8, 9, 10, 11, 12, 20, 21, 22}

    answer = [
        {12, 13, 14, 15, 16, 17, 18, 19},
        {0, 1, 2, 3, 4, 5, 6, 7},
        {22, 23, 24, 25},
        {11, 12},
        {10, 11},
        {9, 10},
        {8, 9},
        {7, 8},
        {21, 22},
        {20, 21},
        {7, 20},
    ]
    assert_components_equal(list(nx.biconnected_components(G)), answer)

    G.add_edge(2, 17)
    pts = set(nx.articulation_points(G))
    assert pts == {7, 20, 21, 22}

