
def test_atanh_series():
    x = Symbol('x')
    assert atanh(x).series(x, 0, 10) == \
        x + x**3/3 + x**5/5 + x**7/7 + x**9/9 + O(x**10)

