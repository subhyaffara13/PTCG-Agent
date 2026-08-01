
def test_derivative_subs2():
    f_func, g_func = symbols('f g', cls=Function)
    f, g = f_func(x, y, z), g_func(x, y, z)
    assert Derivative(f, x, y).subs(Derivative(f, x, y), g) == g
    assert Derivative(f, y, x).subs(Derivative(f, x, y), g) == g
    assert Derivative(f, x, y).subs(Derivative(f, x), g) == Derivative(g, y)
    assert Derivative(f, x, y).subs(Derivative(f, y), g) == Derivative(g, x)
    assert (Derivative(f, x, y, z).subs(
                Derivative(f, x, z), g) == Derivative(g, y))
    assert (Derivative(f, x, y, z).subs(
                Derivative(f, z, y), g) == Derivative(g, x))
    assert (Derivative(f, x, y, z).subs(
                Derivative(f, z, y, x), g) == g)

    # Issue 9135
    assert (Derivative(f, x, x, y).subs(
                Derivative(f, y, y), g) == Derivative(f, x, x, y))
    assert (Derivative(f, x, y, y, z).subs(
                Derivative(f, x, y, y, y), g) == Derivative(f, x, y, y, z))

    assert Derivative(f, x, y).subs(Derivative(f_func(x), x, y), g) == Derivative(f, x, y)

