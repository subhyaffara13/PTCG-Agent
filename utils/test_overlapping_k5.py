
def test_overlapping_K5():
    G = nx.Graph()
    G.add_edges_from(combinations(range(5), 2))  # Add a five clique
    G.add_edges_from(combinations(range(2, 7), 2))  # Add another five clique
    c = list(nx.community.k_clique_communities(G, 4))
    assert c == [frozenset(range(7))]
    c = set(nx.community.k_clique_communities(G, 5))
    assert c == {frozenset(range(5)), frozenset(range(2, 7))}

