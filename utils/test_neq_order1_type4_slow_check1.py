
def test_neq_order1_type4_slow_check1():
    f, g = symbols("f g", cls=Function)
    x = symbols("x")

    eqs = [Eq(diff(f(x), x), x*f(x) + x**2*g(x) + x),
           Eq(diff(g(x), x), 2*x**2*f(x) + (x + 3*x**2)*g(x) + 1)]
    sol = dsolve(eqs)
    assert checksysodesol(eqs, sol) == (True, [0, 0])

