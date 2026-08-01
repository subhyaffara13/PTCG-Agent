
def test_threshold_graph_invalid_creation_sequence():
    bad_creation_sequence = [2.0, 2, 1, 0]  # floats are not allowed
    with pytest.raises(ValueError, match="not a valid creation sequence"):
        nxt.threshold_graph(bad_creation_sequence)

