
def test_halfcauchy_isf(p, expected):
    x = stats.halfcauchy.isf(p)
    assert_allclose(x, expected)

