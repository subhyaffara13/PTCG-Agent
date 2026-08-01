
def test_bug4():
    w = Symbol("w")
    e = x/(w**4 + x**2*w**4 + 2*x*w**4)*w**4
    assert e.nseries(w, n=2).removeO().expand() in [x/(1 + 2*x + x**2),
        1/(1 + x/2 + 1/x/2)/2, 1/x/(1 + 2/x + x**(-2))]

