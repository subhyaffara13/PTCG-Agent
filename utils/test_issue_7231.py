
def test_issue_7231():
    from sympy.abc import a
    ans1 = f(x).series(x, a)
    res = (f(a) + (-a + x)*Subs(Derivative(f(y), y), y, a) +
           (-a + x)**2*Subs(Derivative(f(y), y, y), y, a)/2 +
           (-a + x)**3*Subs(Derivative(f(y), y, y, y),
                            y, a)/6 +
           (-a + x)**4*Subs(Derivative(f(y), y, y, y, y),
                            y, a)/24 +
           (-a + x)**5*Subs(Derivative(f(y), y, y, y, y, y),
                            y, a)/120 + O((-a + x)**6, (x, a)))
    assert res == ans1
    ans2 = f(x).series(x, a)
    assert res == ans2

