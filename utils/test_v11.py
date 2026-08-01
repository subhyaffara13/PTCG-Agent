
def test_V11():
    r1 = integrate(1/(4 + 3*cos(x) + 4*sin(x)), x)
    r2 = factor(r1)
    assert (logcombine(r2, force=True) ==
            log(((tan(x/2) + 1)/(tan(x/2) + 7))**R(1, 3)))

