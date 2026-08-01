
def test_unrad_fail():
    # this only works if we check real_root(eq.subs(x, Rational(1, 3)))
    # but checksol doesn't work like that
    assert solve(root(x**3 - 3*x**2, 3) + 1 - x) == [Rational(1, 3)]
    assert solve(root(x + 1, 3) + root(x**2 - 2, 5) + 1) == [
        -1, -1 + CRootOf(x**5 + x**4 + 5*x**3 + 8*x**2 + 10*x + 5, 0)**3]

