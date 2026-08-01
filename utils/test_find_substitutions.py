
def test_find_substitutions():
    assert find_substitutions((cot(x)**2 + 1)**2*csc(x)**2*cot(x)**2, x, u) == \
        [(cot(x), 1, -u**6 - 2*u**4 - u**2)]
    assert find_substitutions((sec(x)**2 + tan(x) * sec(x)) / (sec(x) + tan(x)),
                              x, u) == [(sec(x) + tan(x), 1, 1/u)]
    assert (-x**2, Rational(-1, 2), exp(u)) in find_substitutions(x * exp(-x**2), x, u)
    assert not find_substitutions(Derivative(f(x), x)**2, x, u)

