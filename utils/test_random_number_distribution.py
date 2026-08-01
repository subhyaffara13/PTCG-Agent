
def test_random_number_distribution():
    # smoke test only
    z = powerlaw_sequence(20, exponent=2.5)
    z = discrete_sequence(20, distribution=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3])

