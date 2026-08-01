
def test_lambdify_imps():
    # Test lambdify with implemented functions
    # first test basic (sympy) lambdify
    f = sympy.cos
    assert lambdify(x, f(x))(0) == 1
    assert lambdify(x, 1 + f(x))(0) == 2
    assert lambdify((x, y), y + f(x))(0, 1) == 2
    # make an implemented function and test
    f = implemented_function("f", lambda x: x + 100)
    assert lambdify(x, f(x))(0) == 100
    assert lambdify(x, 1 + f(x))(0) == 101
    assert lambdify((x, y), y + f(x))(0, 1) == 101
    # Can also handle tuples, lists, dicts as expressions
    lam = lambdify(x, (f(x), x))
    assert lam(3) == (103, 3)
    lam = lambdify(x, [f(x), x])
    assert lam(3) == [103, 3]
    lam = lambdify(x, [f(x), (f(x), x)])
    assert lam(3) == [103, (103, 3)]
    lam = lambdify(x, {f(x): x})
    assert lam(3) == {103: 3}
    lam = lambdify(x, {f(x): x})
    assert lam(3) == {103: 3}
    lam = lambdify(x, {x: f(x)})
    assert lam(3) == {3: 103}
    # Check that imp preferred to other namespaces by default
    d = {'f': lambda x: x + 99}
    lam = lambdify(x, f(x), d)
    assert lam(3) == 103
    # Unless flag passed
    lam = lambdify(x, f(x), d, use_imps=False)
    assert lam(3) == 102

