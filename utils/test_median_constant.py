
def test_median_constant():
    assert median(3) == 3
    x = Symbol('x')
    assert median(x) == x

