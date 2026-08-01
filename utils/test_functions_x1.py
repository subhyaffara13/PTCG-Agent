
def test_functions_X1():
    from sympy.core.function import WildFunction
    x = Symbol('x')
    g = WildFunction('g')
    p = Wild('p')
    q = Wild('q')

    f = cos(5*x)
    assert f.match(p*g(q*x)) == {p: 1, g: cos, q: 5}

