
def test_qs_factor():
    assert qs_factor(1009 * 100003, 2000, 10000) == {1009: 1, 100003: 1}
    n = 1009**2 * 2003**2*30011*400009
    factors = qs_factor(n, 2000, 10000)
    assert len(factors) > 1
    assert math.prod(p**e for p, e in factors.items()) == n

