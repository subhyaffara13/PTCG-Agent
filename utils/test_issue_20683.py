
def test_issue_20683():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    y = Derivative(z, x).subs(x,0)
    assert y.doit() == 0
    y = Derivative(8, x).subs(x,0)
    assert y.doit() == 0

