
def test_cosine_invcdf(p, expected):
    assert_allclose(_cosine_invcdf(p), expected, rtol=1e-14)

