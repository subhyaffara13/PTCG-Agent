
def test_sympy__vector__integrals__ParametricIntegral():
    from sympy.vector.integrals import ParametricIntegral
    from sympy.vector.parametricregion import ParametricRegion
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(ParametricIntegral(C.y*C.i - 10*C.j,\
                    ParametricRegion((x, y), (x, 1, 3), (y, -2, 2))))

