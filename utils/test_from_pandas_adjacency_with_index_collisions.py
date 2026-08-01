
def test_from_pandas_adjacency_with_index_collisions():
    """See gh-7407"""
    df = pd.DataFrame(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ],
        index=[1010001, 2, 1, 1010002],
        columns=[1010001, 2, 1, 1010002],
    )
    G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph)
    expected = nx.DiGraph([(1010001, 2), (2, 1), (1, 1010002)])
    assert nodes_equal(G.nodes, expected.nodes)
    assert edges_equal(G.edges, expected.edges, directed=True)

