
def test_PythonRandomInterface_RandomState():
    np = pytest.importorskip("numpy")

    seed = 42
    rs = np.random.RandomState
    rng = PythonRandomInterface(rs(seed))
    rs42 = rs(seed)

    # make sure these functions are same as expected outcome
    assert rng.randrange(3, 5) == rs42.randint(3, 5)
    assert rng.randrange(2) == rs42.randint(0, 2)
    assert rng.uniform(1, 10) == rs42.uniform(1, 10)
    assert rng.choice([1, 2, 3]) == rs42.choice([1, 2, 3])
    assert rng.gauss(0, 1) == rs42.normal(0, 1)
    assert rng.expovariate(1.5) == rs42.exponential(1 / 1.5)
    assert rng.paretovariate(2) == rs42.pareto(2)
    assert np.all(rng.shuffle([1, 2, 3]) == rs42.shuffle([1, 2, 3]))
    assert np.all(
        rng.sample([1, 2, 3], 2) == rs42.choice([1, 2, 3], (2,), replace=False)
    )
    assert np.all(
        [rng.randint(3, 5) for _ in range(100)]
        == [rs42.randint(3, 6) for _ in range(100)]
    )
    assert rng.random() == rs42.random_sample()

