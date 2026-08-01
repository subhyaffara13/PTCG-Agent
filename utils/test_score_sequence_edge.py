
def test_score_sequence_edge():
    G = DiGraph([(0, 1)])
    assert score_sequence(G) == [0, 1]

