
def test_equality_subs2():
    f = Function('f')
    eq = Eq(f(x)**2, 16)
    assert bool(eq.subs(f(x), 3)) is False
    assert bool(eq.subs(f(x), 4)) is True

