
def test_trig_period():
    x, y = symbols('x, y')

    assert sin(x).period() == 2*pi
    assert cos(x).period() == 2*pi
    assert tan(x).period() == pi
    assert cot(x).period() == pi
    assert sec(x).period() == 2*pi
    assert csc(x).period() == 2*pi
    assert sin(2*x).period() == pi
    assert cot(4*x - 6).period() == pi/4
    assert cos((-3)*x).period() == pi*Rational(2, 3)
    assert cos(x*y).period(x) == 2*pi/abs(y)
    assert sin(3*x*y + 2*pi).period(y) == 2*pi/abs(3*x)
    assert tan(3*x).period(y) is S.Zero
    raises(NotImplementedError, lambda: sin(x**2).period(x))

