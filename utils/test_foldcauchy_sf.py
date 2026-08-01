
def test_foldcauchy_sf(x, c, expected):
    sf = stats.foldcauchy.sf(x, c)
    assert_allclose(sf, expected, 2e-15)

