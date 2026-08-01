
def test_dont_cse_tuples():
    from sympy.core.function import Subs
    f = Function("f")
    g = Function("g")

    name_val, (expr,) = cse(
        Subs(f(x, y), (x, y), (0, 1))
        + Subs(g(x, y), (x, y), (0, 1)))

    assert name_val == []
    assert expr == (Subs(f(x, y), (x, y), (0, 1))
            + Subs(g(x, y), (x, y), (0, 1)))

    name_val, (expr,) = cse(
        Subs(f(x, y), (x, y), (0, x + y))
        + Subs(g(x, y), (x, y), (0, x + y)))

    assert name_val == [(x0, x + y)]
    assert expr == Subs(f(x, y), (x, y), (0, x0)) + \
        Subs(g(x, y), (x, y), (0, x0))

