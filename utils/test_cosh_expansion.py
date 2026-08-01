
def test_cosh_expansion():
    x, y = symbols('x,y')
    assert cosh(x+y).expand(trig=True) == cosh(x)*cosh(y) + sinh(x)*sinh(y)
    assert cosh(2*x).expand(trig=True) == cosh(x)**2 + sinh(x)**2
    assert cosh(3*x).expand(trig=True).expand() == \
        3*sinh(x)**2*cosh(x) + cosh(x)**3

