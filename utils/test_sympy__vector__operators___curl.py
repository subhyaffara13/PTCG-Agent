
def test_sympy__vector__operators__Curl():
    from sympy.vector.operators import Curl
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(Curl(C.i))

