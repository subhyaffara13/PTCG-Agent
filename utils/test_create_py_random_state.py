import random

def test_create_py_random_state():
    pyrs = random.Random

    assert isinstance(create_py_random_state(1), pyrs)
    assert isinstance(create_py_random_state(None), pyrs)
    assert isinstance(create_py_random_state(pyrs(1)), pyrs)
    pytest.raises(ValueError, create_py_random_state, "a")

    np = pytest.importorskip("numpy")

    rs = np.random.RandomState
    rng = np.random.default_rng(1000)
    rng_explicit = np.random.Generator(np.random.SFC64())
    old_nprs = PythonRandomInterface
    nprs = PythonRandomViaNumpyBits
    assert isinstance(create_py_random_state(np.random), nprs)
    assert isinstance(create_py_random_state(rs(1)), old_nprs)
    assert isinstance(create_py_random_state(rng), nprs)
    assert isinstance(create_py_random_state(rng_explicit), nprs)
    # test default rng input
    old_nprs_instance = old_nprs()
    nprs_instance = nprs()
    assert isinstance(old_nprs_instance, old_nprs)
    assert isinstance(nprs_instance, nprs)
    assert create_py_random_state(old_nprs_instance) == old_nprs_instance
    assert create_py_random_state(nprs_instance) == nprs_instance

    # VeryLargeIntegers Smoke test (they raise error for np.random)
    int64max = 9223372036854775807  # from np.iinfo(np.int64).max
    for r in (rng, rs(1)):
        prs = create_py_random_state(r)
        prs.randrange(3, int64max + 5)
        prs.randint(3, int64max + 5)

