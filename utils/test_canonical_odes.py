
def test_canonical_odes():
    f, g, h = symbols('f g h', cls=Function)
    x = symbols('x')
    funcs = [f(x), g(x), h(x)]

    eqs1 = [Eq(f(x).diff(x, x), f(x) + 2*g(x)), Eq(g(x) + 1, g(x).diff(x) + f(x))]
    sol1 = [[Eq(Derivative(f(x), (x, 2)), f(x) + 2*g(x)), Eq(Derivative(g(x), x), -f(x) + g(x) + 1)]]
    assert canonical_odes(eqs1, funcs[:2], x) == sol1

    eqs2 = [Eq(f(x).diff(x), h(x).diff(x) + f(x)), Eq(g(x).diff(x)**2, f(x) + h(x)), Eq(h(x).diff(x), f(x))]
    sol2 = [[Eq(Derivative(f(x), x), 2*f(x)), Eq(Derivative(g(x), x), -sqrt(f(x) + h(x))), Eq(Derivative(h(x), x), f(x))],
            [Eq(Derivative(f(x), x), 2*f(x)), Eq(Derivative(g(x), x), sqrt(f(x) + h(x))), Eq(Derivative(h(x), x), f(x))]]
    assert canonical_odes(eqs2, funcs, x) == sol2

