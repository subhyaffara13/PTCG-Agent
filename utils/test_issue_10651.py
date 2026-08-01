
def test_issue_10651():
    x = Symbol('x', real=True)
    e1 = (-1 + x)/(1 - x)
    e3 = (4*x**2 - 4)/((1 - x)*(1 + x))
    e4 = 1/(cos(x)**2) - (tan(x))**2
    x = Symbol('x', positive=True)
    e5 = (1 + x)/x
    assert e1.is_constant() is None
    assert e3.is_constant() is None
    assert e4.is_constant() is None
    assert e5.is_constant() is False

