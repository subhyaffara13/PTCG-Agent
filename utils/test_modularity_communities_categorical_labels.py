
def test_modularity_communities_categorical_labels(func):
    # Using other than 0-starting contiguous integers as node-labels.
    G = nx.Graph(
        [
            ("a", "b"),
            ("a", "c"),
            ("b", "c"),
            ("b", "d"),  # inter-community edge
            ("d", "e"),
            ("d", "f"),
            ("d", "g"),
            ("f", "g"),
            ("d", "e"),
            ("f", "e"),
        ]
    )
    expected = {frozenset({"f", "g", "e", "d"}), frozenset({"a", "b", "c"})}
    assert set(func(G)) == expected

