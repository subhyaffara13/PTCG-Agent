
def test_CRootOf_evalf_caching_bug():
    r = rootof(x**5 - 5*x + 12, 1)
    r.n()
    a = r._get_interval()
    r = rootof(x**5 - 5*x + 12, 1)
    r.n()
    b = r._get_interval()
    assert a == b

