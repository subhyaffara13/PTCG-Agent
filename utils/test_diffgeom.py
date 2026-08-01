
def test_diffgeom():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField
    x,y = symbols('x y', real=True)
    m = Manifold('M', 2)
    assert str(m) == "M"
    p = Patch('P', m)
    assert str(p) == "P"
    rect = CoordSystem('rect', p, [x, y])
    assert str(rect) == "rect"
    b = BaseScalarField(rect, 0)
    assert str(b) == "x"


def test_diffgeom():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField
    x,y = symbols('x y', real=True)
    m = Manifold('M', 2)
    assert pretty(m) == 'M'
    p = Patch('P', m)
    assert pretty(p) == "P"
    rect = CoordSystem('rect', p, [x, y])
    assert pretty(rect) == "rect"
    b = BaseScalarField(rect, 0)
    assert pretty(b) == "x"

