
def test_sympy__vector__dyadic__DyadicAdd():
    from sympy.vector.dyadic import BaseDyadic, DyadicAdd
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(2 * DyadicAdd(BaseDyadic(C.i, C.i),
                                    BaseDyadic(C.i, C.j)))

