
def test_domain_shift_truncation():
    # center of norm is zero, it should be shifted to the left endpoint of
    # domain. if this was not the case, PINV in UNURAN would raise a warning
    # as the center is not inside the domain
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        rng = FastGeneratorInversion(stats.norm(), domain=(1, 2))
    r = rng.rvs(size=100)
    assert 1 <= r.min() < r.max() <= 2

