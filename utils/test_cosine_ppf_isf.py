
def test_cosine_ppf_isf(p, expected):
    assert_allclose(stats.cosine.ppf(p), expected)
    assert_allclose(stats.cosine.isf(p), -expected)

