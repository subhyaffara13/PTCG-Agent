
def test_degree_sequence_tree_invalid_degree_sequence(deg_seq):
    """Test invalid degree sequences raise an error."""
    with pytest.raises(nx.NetworkXError, match="tree must have"):
        nx.degree_sequence_tree(deg_seq)

