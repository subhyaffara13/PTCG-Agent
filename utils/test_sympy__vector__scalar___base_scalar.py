
def test_sympy__vector__scalar__BaseScalar():
    from sympy.vector.scalar import BaseScalar
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(BaseScalar(0, C, ' ', ' '))

