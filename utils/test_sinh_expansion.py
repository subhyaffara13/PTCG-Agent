
def test_sinh_expansion():
    x, y = symbols('x,y')
    assert sinh(x+y).expand(trig=True) == sinh(x)*cosh(y) + cosh(x)*sinh(y)
    assert sinh(2*x).expand(trig=True) == 2*sinh(x)*cosh(x)
    assert sinh(3*x).expand(trig=True).expand() == \
        sinh(x)**3 + 3*sinh(x)*cosh(x)**2

