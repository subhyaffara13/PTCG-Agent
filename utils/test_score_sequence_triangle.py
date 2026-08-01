
def test_score_sequence_triangle():
    G = DiGraph([(0, 1), (1, 2), (2, 0)])
    assert score_sequence(G) == [1, 1, 1]

