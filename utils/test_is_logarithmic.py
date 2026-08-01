
def test_is_logarithmic():
    assert _is_logarithmic(y, x) is False
    assert _is_logarithmic(log(x), x) is True
    assert _is_logarithmic(log(x) - 3, x) is True
    assert _is_logarithmic(log(x)*log(y), x) is True
    assert _is_logarithmic(log(x)**2, x) is False
    assert _is_logarithmic(log(x - 3) + log(x + 3), x) is True
    assert _is_logarithmic(log(x**y) - y*log(x), x) is True
    assert _is_logarithmic(sin(log(x)), x) is False
    assert _is_logarithmic(x + y, x) is False
    assert _is_logarithmic(log(3*x) - log(1 - x) + 4, x) is True
    assert _is_logarithmic(log(x) + log(y) + x, x) is False
    assert _is_logarithmic(log(log(x - 3)) + log(x - 3), x) is True
    assert _is_logarithmic(log(log(3) + x) + log(x), x) is True
    assert _is_logarithmic(log(x)*(y + 3) + log(x), y) is False

