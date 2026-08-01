
def test_issue_15234():
    x, y = symbols('x y', real=True)
    p = 6*x**5 + x**4 - 4*x**3 + 4*x**2 - 2*x + 3
    p_subbed = 6*x**5 - 4*x**3 - 2*x + y**4 + 4*y**2 + 3
    assert p.subs([(x**i, y**i) for i in [2, 4]]) == p_subbed
    x, y = symbols('x y', complex=True)
    p = 6*x**5 + x**4 - 4*x**3 + 4*x**2 - 2*x + 3
    p_subbed = 6*x**5 - 4*x**3 - 2*x + y**4 + 4*y**2 + 3
    assert p.subs([(x**i, y**i) for i in [2, 4]]) == p_subbed

