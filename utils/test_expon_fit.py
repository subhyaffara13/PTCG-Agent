
def test_expon_fit():
    """gh-6167"""
    data = [0, 0, 0, 0, 2, 2, 2, 2]
    phat = stats.expon.fit(data, floc=0)
    assert_allclose(phat, [0, 1.0], atol=1e-3)

