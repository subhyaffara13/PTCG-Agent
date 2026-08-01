
def test_issue_11806():
    from sympy.core.symbol import symbols
    y, L = symbols('y L', positive=True)
    assert integrate(1/sqrt(x**2 + y**2)**3, (x, -L, L)) == \
        2*L/(y**2*sqrt(L**2 + y**2))

