
def test_FlorySchulz():
    a = Symbol("a")
    z = Symbol("z")
    x = FlorySchulz('x', a)
    assert E(x) == (2 - a)/a
    assert (variance(x) - 2*(1 - a)/a**2).simplify() == S(0)
    assert density(x)(z) == a**2*z*(1 - a)**(z - 1)

