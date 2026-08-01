
def test_docstring_example_connected_dominating_set():
    G = nx.Graph(
        [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 7),
            (3, 8),
            (4, 9),
            (5, 10),
            (6, 11),
            (7, 12),
            (8, 12),
            (9, 12),
            (10, 12),
            (11, 12),
        ]
    )
    assert {1, 2, 3, 4, 5, 6, 7} == nx.connected_dominating_set(G)

