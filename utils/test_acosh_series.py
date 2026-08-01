
def test_acosh_series():
    x = Symbol('x')
    assert acosh(x).series(x, 0, 8) == \
        -I*x + pi*I/2 - I*x**3/6 - 3*I*x**5/40 - 5*I*x**7/112 + O(x**8)
    t5 = acosh(x).taylor_term(5, x)
    assert t5 == - 3*I*x**5/40
    assert acosh(x).taylor_term(7, x, t5, 0) == - 5*I*x**7/112

