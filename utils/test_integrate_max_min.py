
def test_integrate_max_min():
    x = symbols('x', real=True)
    assert integrate(Min(x, 2), (x, 0, 3)) == 4
    assert integrate(Max(x**2, x**3), (x, 0, 2)) == Rational(49, 12)
    assert integrate(Min(exp(x), exp(-x))**2, x) == Piecewise( \
        (exp(2*x)/2, x <= 0), (1 - exp(-2*x)/2, True))
    # issue 7907
    c = symbols('c', extended_real=True)
    int1 = integrate(Max(c, x)*exp(-x**2), (x, -oo, oo))
    int2 = integrate(c*exp(-x**2), (x, -oo, c))
    int3 = integrate(x*exp(-x**2), (x, c, oo))
    assert int1 == int2 + int3 == sqrt(pi)*c*erf(c)/2 + \
        sqrt(pi)*c/2 + exp(-c**2)/2

