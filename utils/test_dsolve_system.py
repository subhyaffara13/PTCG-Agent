
def test_dsolve_system():
    f, g = symbols("f g", cls=Function)
    x = symbols("x")
    eqs = [Eq(f(x).diff(x), f(x) + g(x)), Eq(g(x).diff(x), f(x) + g(x))]
    funcs = [f(x), g(x)]

    sol = [[Eq(f(x), -C1 + C2*exp(2*x)), Eq(g(x), C1 + C2*exp(2*x))]]
    assert dsolve_system(eqs, funcs=funcs, t=x, doit=True) == sol

    raises(ValueError, lambda: dsolve_system(1))
    raises(ValueError, lambda: dsolve_system(eqs, 1))
    raises(ValueError, lambda: dsolve_system(eqs, funcs, 1))
    raises(ValueError, lambda: dsolve_system(eqs, funcs[:1], x))

    eq = (Eq(f(x).diff(x), 12 * f(x) - 6 * g(x)), Eq(g(x).diff(x) ** 2, 11 * f(x) + 3 * g(x)))
    raises(NotImplementedError, lambda: dsolve_system(eq) == ([], []))

    raises(NotImplementedError, lambda: dsolve_system(eq, funcs=[f(x), g(x)]) == ([], []))
    raises(NotImplementedError, lambda: dsolve_system(eq, funcs=[f(x), g(x)], t=x) == ([], []))
    raises(NotImplementedError, lambda: dsolve_system(eq, funcs=[f(x), g(x)], t=x, ics={f(0): 1, g(0): 1}) == ([], []))
    raises(NotImplementedError, lambda: dsolve_system(eq, t=x, ics={f(0): 1, g(0): 1}) == ([], []))
    raises(NotImplementedError, lambda: dsolve_system(eq, ics={f(0): 1, g(0): 1}) == ([], []))
    raises(NotImplementedError, lambda: dsolve_system(eq, funcs=[f(x), g(x)], ics={f(0): 1, g(0): 1}) == ([], []))

