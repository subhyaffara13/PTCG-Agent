
def test_halfcauchy_sf(x, expected):
    sf = stats.halfcauchy.sf(x)
    assert_allclose(sf, expected, 2e-15)

