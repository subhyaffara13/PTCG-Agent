
def test_foldnorm_sf(x, c, expected):
    sf = stats.foldnorm.sf(x, c)
    assert_allclose(sf, expected, 1e-14)

