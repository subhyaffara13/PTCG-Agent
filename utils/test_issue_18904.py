
def test_issue_18904():
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = symbols('x1:16')
    eq = ((x1 & x2 & x3 & x4 & x5 & x6 & x7 & x8 & x9) |
          (x1 & x2 & x3 & x4 & x5 & x6 & x7 & x10 & x9) |
          (x1 & x11 & x3 & x12 & x5 & x13 & x14 & x15 & x9))
    assert is_cnf(to_cnf(eq))
    raises(ValueError, lambda: to_cnf(eq, simplify=True))
    for f, t in zip((And, Or), (to_cnf, to_dnf)):
        eq = f(x1, x2, x3, x4, x5, x6, x7, x8, x9)
        raises(ValueError, lambda: to_cnf(eq, simplify=True))
        assert t(eq, simplify=True, force=True) == eq

