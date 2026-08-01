
def test_random_sequence_low_precision():
    assert nx.utils.cumulative_distribution([0.1] * 100)[-1] == 1.0

