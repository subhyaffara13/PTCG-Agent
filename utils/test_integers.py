
def test_integers():
    Z = S.Integers
    assert 5 in Z
    assert -5 in Z
    assert 5.5 not in Z
    assert not Z.contains(oo)
    assert not Z.contains(-oo)

    zi = iter(Z)
    a, b, c, d = next(zi), next(zi), next(zi), next(zi)
    assert (a, b, c, d) == (0, 1, -1, 2)
    assert isinstance(a, Basic)

    assert Z.intersect(Interval(-5, 5)) == Range(-5, 6)
    assert Z.intersect(Interval(-5, 5, True, True)) == Range(-4, 5)
    assert Z.intersect(Interval(5, S.Infinity)) == Range(5, S.Infinity)
    assert Z.intersect(Interval.Lopen(5, S.Infinity)) == Range(6, S.Infinity)

    assert Z.inf is -oo
    assert Z.sup is oo

    assert Z.boundary == Z
    assert Z.is_open == False
    assert Z.is_closed == True

    assert Z.as_relational(x) == And(Eq(floor(x), x), -oo < x, x < oo)


def test_integers():
    engine = RandomEngine(1, rng=231195739755290648063853336582377368684)

    # basic tests
    sample = engine.integers(1, n=10)
    assert_equal(np.unique(sample), [0])

    assert sample.dtype == np.dtype('int64')

    sample = engine.integers(1, n=10, endpoint=True)
    assert_equal(np.unique(sample), [0, 1])

    low = -5
    high = 7

    # scaling logic
    engine.reset()
    ref_sample = engine.random(20)
    ref_sample = ref_sample * (high - low) + low
    ref_sample = np.floor(ref_sample).astype(np.int64)

    engine.reset()
    sample = engine.integers(low, u_bounds=high, n=20, endpoint=False)

    assert_equal(sample, ref_sample)

    # up to bounds, no less, no more
    sample = engine.integers(low, u_bounds=high, n=100, endpoint=False)
    assert_equal((sample.min(), sample.max()), (low, high-1))

    sample = engine.integers(low, u_bounds=high, n=100, endpoint=True)
    assert_equal((sample.min(), sample.max()), (low, high))

