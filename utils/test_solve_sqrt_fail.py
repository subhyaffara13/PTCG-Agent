
def test_solve_sqrt_fail():
    # this only works if we check real_root(eq.subs(x, Rational(1, 3)))
    # but checksol doesn't work like that
    eq = (x**3 - 3*x**2)**Rational(1, 3) + 1 - x
    assert solveset_real(eq, x) == FiniteSet(Rational(1, 3))

