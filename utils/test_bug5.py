
def test_bug5():
    w = Symbol("w")
    l = Symbol('l')
    e = (-log(w) + log(1 + w*log(x)))**(-2)*w**(-2)*((-log(w) +
        log(1 + x*w))*(-log(w) + log(1 + w*log(x)))*w - x*(-log(w) +
        log(1 + w*log(x)))*w)
    assert e.nseries(w, n=0, logx=l) == x/w/l + 1/w + O(1, w)
    assert e.nseries(w, n=1, logx=l) == x/w/l + 1/w - x/l + 1/l*log(x) \
        + x*log(x)/l**2 + O(w)

