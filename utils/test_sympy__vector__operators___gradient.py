
def test_sympy__vector__operators__Gradient():
    from sympy.vector.operators import Gradient
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(Gradient(C.x))

