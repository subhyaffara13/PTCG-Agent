
def test_restricted_view(G):
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)])
    G.add_node(4)
    H = nx.restricted_view(G, [0, 2, 5], [(1, 2), (3, 4)])
    assert set(H.nodes()) == {1, 3, 4}
    assert set(H.edges()) == {(1, 1)}

