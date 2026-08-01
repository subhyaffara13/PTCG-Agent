
def test_sympy__vector__dyadic__BaseDyadic():
    from sympy.vector.dyadic import BaseDyadic
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(BaseDyadic(C.i, C.j))

