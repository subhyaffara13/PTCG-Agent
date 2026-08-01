
def test_random_state():
    # fixed seed
    gen = FastGeneratorInversion(stats.norm(), random_state=68734509)
    x1 = gen.rvs(size=10)
    gen.random_state = 68734509
    x2 = gen.rvs(size=10)
    assert_array_equal(x1, x2)

    # Generator
    urng = np.random.default_rng(20375857)
    gen = FastGeneratorInversion(stats.norm(), random_state=urng)
    x1 = gen.rvs(size=10)
    gen.random_state = np.random.default_rng(20375857)
    x2 = gen.rvs(size=10)
    assert_array_equal(x1, x2)

    # RandomState
    urng = np.random.RandomState(2364)
    gen = FastGeneratorInversion(stats.norm(), random_state=urng)
    x1 = gen.rvs(size=10)
    gen.random_state = np.random.RandomState(2364)
    x2 = gen.rvs(size=10)
    assert_array_equal(x1, x2)

    # if evaluate_error is called, it must not interfere with the random_state
    # used by rvs
    gen = FastGeneratorInversion(stats.norm(), random_state=68734509)
    x1 = gen.rvs(size=10)
    _ = gen.evaluate_error(size=5)  # this will generate 5 uniform rvs
    x2 = gen.rvs(size=10)
    gen.random_state = 68734509
    x3 = gen.rvs(size=20)
    assert_array_equal(x2, x3[10:])


def test_random_state(method, kwargs):
    Method = getattr(stats.sampling, method)

    # simple seed that works for any version of NumPy
    seed = 123
    rng1 = Method(**kwargs, random_state=seed)
    rng2 = Method(**kwargs, random_state=seed)
    assert_equal(rng1.rvs(100), rng2.rvs(100))

    # global seed
    rng = np.random.RandomState(123)
    rng1 = Method(**kwargs)
    rvs1 = rng1.rvs(100, random_state=rng)
    np.random.seed(None)  # valid use of np.random.seed
    rng2 = Method(**kwargs, random_state=123)
    rvs2 = rng2.rvs(100)
    assert_equal(rvs1, rvs2)

    # Generator seed for new NumPy
    # when a RandomState is given, it should take the bitgen_t
    # member of the class and create a Generator instance.
    seed1 = np.random.RandomState(np.random.MT19937(123))
    seed2 = np.random.Generator(np.random.MT19937(123))
    rng1 = Method(**kwargs, random_state=seed1)
    rng2 = Method(**kwargs, random_state=seed2)
    assert_equal(rng1.rvs(100), rng2.rvs(100))

