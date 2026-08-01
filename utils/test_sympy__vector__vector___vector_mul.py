
def test_sympy__vector__vector__VectorMul():
    from sympy.vector.vector import VectorMul
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    from sympy.abc import a
    assert _test_args(VectorMul(a, C.i))

