
def test_neq_order1_type4_slow_check2():
    f, g, h = symbols("f, g, h", cls=Function)
    x = Symbol("x")

    eqs = [
        Eq(Derivative(f(x), x), x*h(x) + f(x) + g(x) + 1),
        Eq(Derivative(g(x), x), x*g(x) + f(x) + h(x) + 10),
        Eq(Derivative(h(x), x), x*f(x) + x + g(x) + h(x))
    ]
    with dotprodsimp(True):
        sol = dsolve(eqs)
    assert checksysodesol(eqs, sol) == (True, [0, 0, 0])

