
def test_cosine_cdf_sf(x, expected):
    assert_allclose(stats.cosine.cdf(x), expected)
    assert_allclose(stats.cosine.sf(-x), expected)

