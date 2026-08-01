
def test_dsolve():

    f, g = symbols('f g', cls=Function)
    x, y = symbols('x y')

    eqs = [f(x).diff(x) - x, f(x).diff(x) + x]
    with raises(ValueError):
        dsolve(eqs)

    eqs = [f(x, y).diff(x)]
    with raises(ValueError):
        dsolve(eqs)

    eqs = [f(x, y).diff(x)+g(x).diff(x), g(x).diff(x)]
    with raises(ValueError):
        dsolve(eqs)

