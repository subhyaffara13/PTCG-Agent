
def test_domain_check():
    assert domain_check(1/(1 + (1/(x+1))**2), x, -1) is False
    assert domain_check(x**2, x, 0) is True
    assert domain_check(x, x, oo) is False
    assert domain_check(0, x, oo) is False

