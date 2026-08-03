from typing import Tuple

def test_as_poly_as_expr():
    f = x**2 + 2*x*y

    assert f.as_poly().as_expr() == f
    assert f.as_poly(x, y).as_expr() == f

    assert (f + sin(x)).as_poly(x, y) is None

    p = Poly(f, x, y)

    assert p.as_poly() == p

    # https://github.com/sympy/sympy/issues/20610
    assert S(2).as_poly() is None
    assert sqrt(2).as_poly(extension=True) is None

    raises(AttributeError, lambda: Tuple(x, x).as_poly(x))
    raises(AttributeError, lambda: Tuple(x ** 2, x, y).as_poly(x))

