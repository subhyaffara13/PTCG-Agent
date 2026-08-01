
def test_multigraph_keys():
    """Tests that multiedge keys are reset in new graph."""
    G = nx.path_graph(3, create_using=nx.MultiGraph())
    G.add_edge(0, 1, 5)
    G.add_edge(0, 0, 0)
    G.add_edge(0, 2, 5)
    actual = nx.contracted_nodes(G, 0, 2)
    expected = nx.MultiGraph()
    expected.add_edge(0, 1, 0)
    expected.add_edge(0, 1, 5)
    expected.add_edge(0, 1, 2)  # keyed as 2 b/c 2 edges already in G
    expected.add_edge(0, 0, 0)
    expected.add_edge(0, 0, 1)  # this comes from (0, 2, 5)
    assert edges_equal(actual.edges, expected.edges)

