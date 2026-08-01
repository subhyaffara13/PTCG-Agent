
def test_issue_14608():
    a, b = symbols('a b', commutative=False)
    x, y = symbols('x y')
    raises(AttributeError, lambda: collect(a*b + b*a, a))
    assert collect(x*y + y*(x+1), a) == x*y + y*(x+1)
    assert collect(x*y + y*(x+1) + a*b + b*a, y) == y*(2*x + 1) + a*b + b*a

