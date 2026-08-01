
def test_degree_sequence_tree(deg_seq):
    G = nx.degree_sequence_tree(deg_seq)
    assert sorted(dict(G.degree).values()) == sorted(deg_seq)
    assert nx.is_tree(G)

