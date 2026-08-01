
def test_cosine_cdf(x, expected):
    assert_allclose(_cosine_cdf(x), expected, rtol=5e-15)

