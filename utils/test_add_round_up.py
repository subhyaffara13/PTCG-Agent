
def test_add_round_up():
    rng = np.random.RandomState(1234)
    _test_internal.test_add_round(10**5, 'up', rng)

