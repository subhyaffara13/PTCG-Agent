
def test_acsch_series():
    x = Symbol('x')
    assert acsch(x).series(x, 0, 9) == log(2) - log(x) + x**2/4 - 3*x**4/32 \
    + 5*x**6/96 - 35*x**8/1024 + O(x**9)
    t4 = acsch(x).taylor_term(4, x)
    assert t4 == -3*x**4/32
    assert acsch(x).taylor_term(6, x, t4, 0) == 5*x**6/96

