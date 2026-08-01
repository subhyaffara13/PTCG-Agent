
def test_log3():
    l = Symbol('l')
    e = 1/log(-1/x)
    assert e.nseries(x, n=4, logx=l) == 1/(-l + log(-1))

