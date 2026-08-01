
def test_invweibull_isf(p, c, expected):
    computed = stats.invweibull.isf(p, c)
    assert_allclose(computed, expected, rtol=1e-15)

