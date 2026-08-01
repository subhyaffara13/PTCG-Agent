
def test_asec_series():
    assert asec(x).series(x, 0, 9) == \
        I*log(2) - I*log(x) - I*x**2/4 - 3*I*x**4/32 \
        - 5*I*x**6/96 - 35*I*x**8/1024 + O(x**9)
    t4 = asec(x).taylor_term(4, x)
    assert t4 == -3*I*x**4/32
    assert asec(x).taylor_term(6, x, t4, 0) == -5*I*x**6/96

