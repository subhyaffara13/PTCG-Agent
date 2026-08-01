
def test_integrals():
    x = Symbol("x")
    for c in (Integral, Integral(x)):
        check(c)

