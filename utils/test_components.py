
def test_components():
    assert components(x*y, x) == {x}
    assert components(1/(x + y), x) == {x}
    assert components(sin(x), x) == {sin(x), x}
    assert components(sin(x)*sqrt(log(x)), x) == \
        {log(x), sin(x), sqrt(log(x)), x}
    assert components(x*sin(exp(x)*y), x) == \
        {sin(y*exp(x)), x, exp(x)}
    assert components(x**Rational(17, 54)/sqrt(sin(x)), x) == \
        {sin(x), x**Rational(1, 54), sqrt(sin(x)), x}

    assert components(f(x), x) == \
        {x, f(x)}
    assert components(Derivative(f(x), x), x) == \
        {x, f(x), Derivative(f(x), x)}
    assert components(f(x)*diff(f(x), x), x) == \
        {x, f(x), Derivative(f(x), x), Derivative(f(x), x)}

