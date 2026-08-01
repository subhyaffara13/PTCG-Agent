
def test_simplify_function_inverse():
    # "inverse" attribute does not guarantee that f(g(x)) is x
    # so this simplification should not happen automatically.
    # See issue #12140
    x, y = symbols('x, y')
    g = Function('g')

    class f(Function):
        def inverse(self, argindex=1):
            return g

    assert simplify(f(g(x))) == f(g(x))
    assert inversecombine(f(g(x))) == x
    assert simplify(f(g(x)), inverse=True) == x
    assert simplify(f(g(sin(x)**2 + cos(x)**2)), inverse=True) == 1
    assert simplify(f(g(x, y)), inverse=True) == f(g(x, y))
    assert unchanged(asin, sin(x))
    assert simplify(asin(sin(x))) == asin(sin(x))
    assert simplify(2*asin(sin(3*x)), inverse=True) == 6*x
    assert simplify(log(exp(x))) == log(exp(x))
    assert simplify(log(exp(x)), inverse=True) == x
    assert simplify(exp(log(x)), inverse=True) == x
    assert simplify(log(exp(x), 2), inverse=True) == x/log(2)
    assert simplify(log(exp(x), 2, evaluate=False), inverse=True) == x/log(2)

