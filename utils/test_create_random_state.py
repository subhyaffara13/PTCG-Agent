
def test_create_random_state():
    np = pytest.importorskip("numpy")
    rs = np.random.RandomState

    assert isinstance(create_random_state(1), rs)
    assert isinstance(create_random_state(None), rs)
    assert isinstance(create_random_state(np.random), rs)
    assert isinstance(create_random_state(rs(1)), rs)
    # Support for numpy.random.Generator
    rng = np.random.default_rng()
    assert isinstance(create_random_state(rng), np.random.Generator)
    pytest.raises(ValueError, create_random_state, "a")

    assert np.all(rs(1).rand(10) == create_random_state(1).rand(10))

