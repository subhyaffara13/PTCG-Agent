
def test_issue_3940():
    a, b, c, d = symbols('a:d', positive=True)
    assert integrate(exp(-x**2 + I*c*x), x) == \
        -sqrt(pi)*exp(-c**2/4)*erf(I*c/2 - x)/2
    assert integrate(exp(a*x**2 + b*x + c), x).equals(
        sqrt(pi)*exp(c - b**2/(4*a))*erfi((2*a*x + b)/(2*sqrt(a)))/(2*sqrt(a)))

    from sympy.core.function import expand_mul
    from sympy.abc import k
    assert expand_mul(integrate(exp(-x**2)*exp(I*k*x), (x, -oo, oo))) == \
        sqrt(pi)*exp(-k**2/4)
    a, d = symbols('a d', positive=True)
    assert expand_mul(integrate(exp(-a*x**2 + 2*d*x), (x, -oo, oo))) == \
        sqrt(pi)*exp(d**2/a)/sqrt(a)

