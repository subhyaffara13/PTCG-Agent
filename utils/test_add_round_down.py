
def test_add_round_down():
    rng = np.random.RandomState(1234)
    _test_internal.test_add_round(10**5, 'down', rng)

