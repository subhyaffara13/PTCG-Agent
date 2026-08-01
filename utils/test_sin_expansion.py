
def test_sin_expansion():
    # Note: these formulas are not unique.  The ones here come from the
    # Chebyshev formulas.
    assert sin(x + y).expand(trig=True) == sin(x)*cos(y) + cos(x)*sin(y)
    assert sin(x - y).expand(trig=True) == sin(x)*cos(y) - cos(x)*sin(y)
    assert sin(y - x).expand(trig=True) == cos(x)*sin(y) - sin(x)*cos(y)
    assert sin(2*x).expand(trig=True) == 2*sin(x)*cos(x)
    assert sin(3*x).expand(trig=True) == -4*sin(x)**3 + 3*sin(x)
    assert sin(4*x).expand(trig=True) == -8*sin(x)**3*cos(x) + 4*sin(x)*cos(x)
    assert sin(2*pi/17).expand(trig=True) == sin(2*pi/17, evaluate=False)
    assert sin(x+pi/17).expand(trig=True) == sin(pi/17)*cos(x) + cos(pi/17)*sin(x)
    _test_extrig(sin, 2, 2*sin(1)*cos(1))
    _test_extrig(sin, 3, -4*sin(1)**3 + 3*sin(1))

