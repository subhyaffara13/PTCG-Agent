
def test_sympy__vector__vector__BaseVector():
    from sympy.vector.vector import BaseVector
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(BaseVector(0, C, ' ', ' '))

