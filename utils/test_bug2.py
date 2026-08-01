
def test_bug2():  # 1/log(0)*log(0) problem
    w = Symbol("w")
    e = (w**(-1) + w**(
        -log(3)*log(2)**(-1)))**(-1)*(3*w**(-log(3)*log(2)**(-1)) + 2*w**(-1))
    e = e.expand()
    assert e.nseries(w, 0, 4).subs(w, 0) == 3

