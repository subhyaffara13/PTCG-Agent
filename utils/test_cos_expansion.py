
def test_cos_expansion():
    assert cos(x + y).expand(trig=True) == cos(x)*cos(y) - sin(x)*sin(y)
    assert cos(x - y).expand(trig=True) == cos(x)*cos(y) + sin(x)*sin(y)
    assert cos(y - x).expand(trig=True) == cos(x)*cos(y) + sin(x)*sin(y)
    assert cos(2*x).expand(trig=True) == 2*cos(x)**2 - 1
    assert cos(3*x).expand(trig=True) == 4*cos(x)**3 - 3*cos(x)
    assert cos(4*x).expand(trig=True) == 8*cos(x)**4 - 8*cos(x)**2 + 1
    assert cos(2*pi/17).expand(trig=True) == cos(2*pi/17, evaluate=False)
    assert cos(x+pi/17).expand(trig=True) == cos(pi/17)*cos(x) - sin(pi/17)*sin(x)
    _test_extrig(cos, 2, 2*cos(1)**2 - 1)
    _test_extrig(cos, 3, 4*cos(1)**3 - 3*cos(1))

