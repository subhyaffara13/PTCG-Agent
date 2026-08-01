
def test_asech_series():
    x = Symbol('x')
    assert asech(x).series(x, 0, 9, cdir=1) == log(2) - log(x) - x**2/4 - 3*x**4/32 \
    - 5*x**6/96 - 35*x**8/1024 + O(x**9)
    assert asech(x).series(x, 0, 9, cdir=-1) == I*pi + log(2) - log(-x) - x**2/4 - \
    3*x**4/32 - 5*x**6/96 - 35*x**8/1024 + O(x**9)
    t6 = asech(x).taylor_term(6, x)
    assert t6 == -5*x**6/96
    assert asech(x).taylor_term(8, x, t6, 0) == -35*x**8/1024

