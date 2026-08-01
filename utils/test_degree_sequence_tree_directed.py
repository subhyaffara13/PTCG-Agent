
def test_degree_sequence_tree_directed(graph_type):
    with pytest.raises(nx.NetworkXError, match="Directed Graph not supported"):
        nx.degree_sequence_tree([1, 1], create_using=graph_type())

