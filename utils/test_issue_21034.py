
def test_issue_21034():
    a = symbols('a', real=True)
    system = [x - cosh(cos(4)), y - sinh(cos(a)), z - tanh(x)]
    # constants inside hyperbolic functions should not be rewritten in terms of exp
    assert solve(system, x, y, z) == [(cosh(cos(4)), sinh(cos(a)), tanh(cosh(cos(4))))]
    # but if the variable of interest is present in a hyperbolic function,
    # then it should be rewritten in terms of exp and solved further
    newsystem = [(exp(x) - exp(-x)) - tanh(x)*(exp(x) + exp(-x)) + x - 5]
    assert solve(newsystem, x) == {x: 5}


def test_issue_21034():
    x = Symbol('x', real=True, nonzero=True)
    f1 = x*(-x**4/asin(5)**4 - x*sinh(x + log(asin(5))) + 5)
    f2 = (x + cosh(cos(4)))/(x*(x + 1/(12*x)))

    assert integrate(f1, x) == \
        -x**6/(6*asin(5)**4) - x**2*cosh(x + log(asin(5))) + 5*x**2/2 + 2*x*sinh(x + log(asin(5))) - 2*cosh(x + log(asin(5)))

    assert integrate(f2, x) == \
        log(x**2 + S(1)/12)/2 + 2*sqrt(3)*cosh(cos(4))*atan(2*sqrt(3)*x)


def test_issue_21034():
    e = -I*log((re(asin(5)) + I*im(asin(5)))/sqrt(re(asin(5))**2 + im(asin(5))**2))/pi
    assert e.round(2)

