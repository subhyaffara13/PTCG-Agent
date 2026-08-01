
def test_is_exponential():
    assert _is_exponential(y, x) is False
    assert _is_exponential(3**x - 2, x) is True
    assert _is_exponential(5**x - 7**(2 - x), x) is True
    assert _is_exponential(sin(2**x) - 4*x, x) is False
    assert _is_exponential(x**y - z, y) is True
    assert _is_exponential(x**y - z, x) is False
    assert _is_exponential(2**x + 4**x - 1, x) is True
    assert _is_exponential(x**(y*z) - x, x) is False
    assert _is_exponential(x**(2*x) - 3**x, x) is False
    assert _is_exponential(x**y - y*z, y) is False
    assert _is_exponential(x**y - x*z, y) is True

