
def test_old_issues():
    # https://github.com/sympy/sympy/issues/5212
    I1 = integrate(cos(log(x**2))/x)
    assert I1 == sin(log(x**2))/2
    # https://github.com/sympy/sympy/issues/5462
    I2 = integrate(1/(x**2+y**2)**(Rational(3,2)),x)
    assert I2 == x/(y**3*sqrt(x**2/y**2 + 1))
    # https://github.com/sympy/sympy/issues/6278
    I3 = integrate(1/(cos(x)+2),(x,0,2*pi))
    assert I3 == 2*sqrt(3)*pi/3

