
def test_invweibull_sf(x, c, expected):
    computed = stats.invweibull.sf(x, c)
    assert_allclose(computed, expected, rtol=1e-15)

