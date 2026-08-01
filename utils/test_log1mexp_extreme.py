
def test_log1mexp_extreme(x, expected):
    observed = _log1mexp(x)
    assert_equal(expected, observed)

