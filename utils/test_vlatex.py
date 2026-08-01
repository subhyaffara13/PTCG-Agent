
def test_vlatex(): # vlatex is broken #12078
    from sympy.physics.vector import vlatex

    x = symbols('x')
    J = symbols('J')

    f = Function('f')
    g = Function('g')
    h = Function('h')

    expected = r'J \left(\frac{d}{d x} g{\left(x \right)} - \frac{d}{d x} h{\left(x \right)}\right)'

    expr = J*f(x).diff(x).subs(f(x), g(x)-h(x))

    assert vlatex(expr) == expected

