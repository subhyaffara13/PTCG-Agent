
def test_graph_is_tournament():
    for _ in range(10):
        G = random_tournament(5)
        assert is_tournament(G)

