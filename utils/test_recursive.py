
def test_recursive():
    from sympy.core.symbol import symbols
    a, b, c = symbols('a b c', positive=True)
    r = exp(-(x - a)**2)*exp(-(x - b)**2)
    e = integrate(r, (x, 0, oo), meijerg=True)
    assert simplify(e.expand()) == (
        sqrt(2)*sqrt(pi)*(
        (erf(sqrt(2)*(a + b)/2) + 1)*exp(-a**2/2 + a*b - b**2/2))/4)
    e = integrate(exp(-(x - a)**2)*exp(-(x - b)**2)*exp(c*x), (x, 0, oo), meijerg=True)
    assert simplify(e) == (
        sqrt(2)*sqrt(pi)*(erf(sqrt(2)*(2*a + 2*b + c)/4) + 1)*exp(-a**2 - b**2
        + (2*a + 2*b + c)**2/8)/4)
    assert simplify(integrate(exp(-(x - a - b - c)**2), (x, 0, oo), meijerg=True)) == \
        sqrt(pi)/2*(1 + erf(a + b + c))
    assert simplify(integrate(exp(-(x + a + b + c)**2), (x, 0, oo), meijerg=True)) == \
        sqrt(pi)/2*(1 - erf(a + b + c))

