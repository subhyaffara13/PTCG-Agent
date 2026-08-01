
def test_as_ordered_terms():

    assert x.as_ordered_terms() == [x]
    assert (sin(x)**2*cos(x) + sin(x)*cos(x)**2 + 1).as_ordered_terms() \
        == [sin(x)**2*cos(x), sin(x)*cos(x)**2, 1]

    args = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    expr = Add(*args)

    assert expr.as_ordered_terms() == args

    assert (1 + 4*sqrt(3)*pi*x).as_ordered_terms() == [4*pi*x*sqrt(3), 1]

    assert ( 2 + 3*I).as_ordered_terms() == [2, 3*I]
    assert (-2 + 3*I).as_ordered_terms() == [-2, 3*I]
    assert ( 2 - 3*I).as_ordered_terms() == [2, -3*I]
    assert (-2 - 3*I).as_ordered_terms() == [-2, -3*I]

    assert ( 4 + 3*I).as_ordered_terms() == [4, 3*I]
    assert (-4 + 3*I).as_ordered_terms() == [-4, 3*I]
    assert ( 4 - 3*I).as_ordered_terms() == [4, -3*I]
    assert (-4 - 3*I).as_ordered_terms() == [-4, -3*I]

    e = x**2*y**2 + x*y**4 + y + 2

    assert e.as_ordered_terms(order="lex") == [x**2*y**2, x*y**4, y, 2]
    assert e.as_ordered_terms(order="grlex") == [x*y**4, x**2*y**2, y, 2]
    assert e.as_ordered_terms(order="rev-lex") == [2, y, x*y**4, x**2*y**2]
    assert e.as_ordered_terms(order="rev-grlex") == [2, y, x**2*y**2, x*y**4]

    k = symbols('k')
    assert k.as_ordered_terms(data=True) == ([(k, ((1.0, 0.0), (1,), ()))], [k])

