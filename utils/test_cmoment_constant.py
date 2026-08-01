
def test_cmoment_constant():
    assert variance(3) == 0
    assert cmoment(3, 3) == 0
    assert cmoment(3, 4) == 0
    x = Symbol('x')
    assert variance(x) == 0
    assert cmoment(x, 15) == 0
    assert cmoment(x, 0) == 1

