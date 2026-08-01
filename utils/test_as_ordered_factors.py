
def test_as_ordered_factors():

    assert x.as_ordered_factors() == [x]
    assert (2*x*x**n*sin(x)*cos(x)).as_ordered_factors() \
        == [Integer(2), x, x**n, sin(x), cos(x)]

    args = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    expr = Mul(*args)

    assert expr.as_ordered_factors() == args

    A, B = symbols('A,B', commutative=False)

    assert (A*B).as_ordered_factors() == [A, B]
    assert (B*A).as_ordered_factors() == [B, A]

