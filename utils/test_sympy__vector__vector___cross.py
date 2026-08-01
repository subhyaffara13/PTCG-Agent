
def test_sympy__vector__vector__Cross():
    from sympy.vector.vector import Cross
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    _test_args(Cross(C.i, C.j))

