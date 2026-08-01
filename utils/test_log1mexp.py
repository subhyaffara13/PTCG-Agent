
def test_log1mexp(x, expected):
    observed = _log1mexp(x)
    assert_allclose(observed, expected, rtol=1e-15, atol=1e-300)

