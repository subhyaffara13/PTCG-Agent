
def test_issue_8458():
    x, y = symbols('x y')
    # Original issue
    p1 = Piecewise((0, Eq(x, 0)), (sin(x), True))
    assert p1.simplify() == sin(x)
    # Slightly larger variant
    p2 = Piecewise((x, Eq(x, 0)), (4*x + (y-2)**4, Eq(x, 0) & Eq(x+y, 2)), (sin(x), True))
    assert p2.simplify() == sin(x)
    # Test for problem highlighted during review
    p3 = Piecewise((x+1, Eq(x, -1)), (4*x + (y-2)**4, Eq(x, 0) & Eq(x+y, 2)), (sin(x), True))
    assert p3.simplify() == Piecewise((0, Eq(x, -1)), (sin(x), True))

