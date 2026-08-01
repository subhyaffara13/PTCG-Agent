
def test_Piecewise_replace_relational_27538():
    x, y = symbols('x, y')
    p1 = Piecewise(
        (0, Eq(x, True)),
        (1, True),
    )
    p2 = p1.xreplace({x: y < 1})
    assert p2.subs(y, 0) == 0
    assert p2.subs(y, 1) == 1

