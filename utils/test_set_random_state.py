
def test_set_random_state():
    rng1 = TransformedDensityRejection(StandardNormal(), random_state=123)
    rng2 = TransformedDensityRejection(StandardNormal())
    rng2.set_random_state(123)
    assert_equal(rng1.rvs(100), rng2.rvs(100))
    rng = TransformedDensityRejection(StandardNormal(), random_state=123)
    rvs1 = rng.rvs(100)
    rng.set_random_state(123)
    rvs2 = rng.rvs(100)
    assert_equal(rvs1, rvs2)

