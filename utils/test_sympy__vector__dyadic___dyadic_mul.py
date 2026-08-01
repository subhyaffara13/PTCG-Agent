
def test_sympy__vector__dyadic__DyadicMul():
    from sympy.vector.dyadic import BaseDyadic, DyadicMul
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(DyadicMul(3, BaseDyadic(C.i, C.j)))

