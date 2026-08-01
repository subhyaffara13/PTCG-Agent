
def test_ispath(G):
    G.add_edges_from([(1, 2), (2, 3), (1, 2), (3, 4)])
    valid_path = [1, 2, 3, 4]
    invalid_path = [1, 2, 4, 3]  # wrong node order
    another_invalid_path = [1, 2, 3, 4, 5]  # contains node not in G
    assert nx.is_path(G, valid_path)
    assert not nx.is_path(G, invalid_path)
    assert not nx.is_path(G, another_invalid_path)

