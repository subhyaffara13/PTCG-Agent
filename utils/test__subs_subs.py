
def test_Subs_subs():
    assert Subs(x*y, x, x).subs(x, y) == Subs(x*y, x, y)
    assert Subs(x*y, x, x + 1).subs(x, y) == \
        Subs(x*y, x, y + 1)
    assert Subs(x*y, y, x + 1).subs(x, y) == \
        Subs(y**2, y, y + 1)
    a = Subs(x*y*z, (y, x, z), (x + 1, x + z, x))
    b = Subs(x*y*z, (y, x, z), (x + 1, y + z, y))
    assert a.subs(x, y) == b and \
        a.doit().subs(x, y) == a.subs(x, y).doit()
    f = Function('f')
    g = Function('g')
    assert Subs(2*f(x, y) + g(x), f(x, y), 1).subs(y, 2) == Subs(
        2*f(x, y) + g(x), (f(x, y), y), (1, 2))

