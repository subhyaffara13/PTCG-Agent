
def test_sympy__vector__operators__Divergence():
    from sympy.vector.operators import Divergence
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(Divergence(C.i))

