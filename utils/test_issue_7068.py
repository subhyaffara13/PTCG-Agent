
def test_issue_7068():
    from sympy.abc import a, b
    f = Function('f')
    y1 = Dummy('y')
    y2 = Dummy('y')
    func1 = f(a + y1 * b)
    func2 = f(a + y2 * b)
    func1_y = func1.diff(y1)
    func2_y = func2.diff(y2)
    assert func1_y != func2_y
    z1 = Subs(f(a), a, y1)
    z2 = Subs(f(a), a, y2)
    assert z1 != z2

