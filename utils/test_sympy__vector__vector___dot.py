
def test_sympy__vector__vector__Dot():
    from sympy.vector.vector import Dot
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    _test_args(Dot(C.i, C.j))

