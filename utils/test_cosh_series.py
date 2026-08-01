
def test_cosh_series():
    x = Symbol('x')
    assert cosh(x).series(x, 0, 10) == \
        1 + x**2/2 + x**4/24 + x**6/720 + x**8/40320 + O(x**10)

