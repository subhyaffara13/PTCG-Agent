
def test_asinh_series():
    x = Symbol('x')
    assert asinh(x).series(x, 0, 8) == \
        x - x**3/6 + 3*x**5/40 - 5*x**7/112 + O(x**8)
    t5 = asinh(x).taylor_term(5, x)
    assert t5 == 3*x**5/40
    assert asinh(x).taylor_term(7, x, t5, 0) == -5*x**7/112

