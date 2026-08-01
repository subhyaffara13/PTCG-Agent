
def test_deterministic(engine):
    seed_number = 2359834584

    rng = np.random.RandomState(seed_number)
    res1 = engine(d=1, seed=rng).random(4)
    rng = np.random.RandomState(seed_number)
    res2 = engine(d=1, seed=rng).random(4)
    assert_equal(res1, res2)

    rng = np.random.default_rng(seed_number)
    res1 = engine(d=1, seed=rng).random(4)
    res2 = engine(d=1, rng=seed_number).random(4)
    assert_equal(res1, res2)
    rng = np.random.default_rng(seed_number)
    res3 = engine(d=1, rng=rng).random(4)
    assert_equal(res2, res1)
    assert_equal(res3, res1)

    message = "got multiple values for argument now known as `rng`"
    with pytest.raises(TypeError, match=message):
        engine(d=1, rng=seed_number, seed=seed_number)

