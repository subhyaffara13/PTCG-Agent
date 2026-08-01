
def test_sinh_series():
    x = Symbol('x')
    assert sinh(x).series(x, 0, 10) == \
        x + x**3/6 + x**5/120 + x**7/5040 + x**9/362880 + O(x**10)

