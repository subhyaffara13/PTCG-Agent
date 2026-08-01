
def test_acsc_series():
    assert acsc(x).series(x, 0, 9) == \
        -I*log(2) + pi/2 + I*log(x) + I*x**2/4 \
        + 3*I*x**4/32 + 5*I*x**6/96 + 35*I*x**8/1024 + O(x**9)
    t6 = acsc(x).taylor_term(6, x)
    assert t6 == 5*I*x**6/96
    assert acsc(x).taylor_term(8, x, t6, 0) == 35*I*x**8/1024

