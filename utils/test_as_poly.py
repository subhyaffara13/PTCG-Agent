
def test_as_poly():
    from sympy.polys.polytools import Poly
    # Only Eq should have an as_poly method:
    assert Eq(x, 1).as_poly() == Poly(x - 1, x, domain='ZZ')
    raises(AttributeError, lambda: Ne(x, 1).as_poly())
    raises(AttributeError, lambda: Ge(x, 1).as_poly())
    raises(AttributeError, lambda: Gt(x, 1).as_poly())
    raises(AttributeError, lambda: Le(x, 1).as_poly())
    raises(AttributeError, lambda: Lt(x, 1).as_poly())

