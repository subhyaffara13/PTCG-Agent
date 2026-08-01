
def test_manualintegrate_Heaviside():
    assert_is_integral_of(DiracDelta(3*x+2), Heaviside(3*x+2)/3)
    assert_is_integral_of(DiracDelta(3*x, 0), Heaviside(3*x)/3)
    assert manualintegrate(DiracDelta(a+b*x, 1), x) == \
        Piecewise((DiracDelta(a + b*x)/b, Ne(b, 0)), (x*DiracDelta(a, 1), True))
    assert_is_integral_of(DiracDelta(x/3-1, 2), 3*DiracDelta(x/3-1, 1))
    assert manualintegrate(Heaviside(x), x) == x*Heaviside(x)
    assert manualintegrate(x*Heaviside(2), x) == x**2/2
    assert manualintegrate(x*Heaviside(-2), x) == 0
    assert manualintegrate(x*Heaviside( x), x) == x**2*Heaviside( x)/2
    assert manualintegrate(x*Heaviside(-x), x) == x**2*Heaviside(-x)/2
    assert manualintegrate(Heaviside(2*x + 4), x) == (x+2)*Heaviside(2*x + 4)
    assert manualintegrate(x*Heaviside(x), x) == x**2*Heaviside(x)/2
    assert manualintegrate(Heaviside(x + 1)*Heaviside(1 - x)*x**2, x) == \
        ((x**3/3 + Rational(1, 3))*Heaviside(x + 1) - Rational(2, 3))*Heaviside(-x + 1)

    y = Symbol('y')
    assert manualintegrate(sin(7 + x)*Heaviside(3*x - 7), x) == \
            (- cos(x + 7) + cos(Rational(28, 3)))*Heaviside(3*x - S(7))

    assert manualintegrate(sin(y + x)*Heaviside(3*x - y), x) == \
            (cos(y*Rational(4, 3)) - cos(x + y))*Heaviside(3*x - y)

