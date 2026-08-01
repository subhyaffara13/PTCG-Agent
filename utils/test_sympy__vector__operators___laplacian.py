
def test_sympy__vector__operators__Laplacian():
    from sympy.vector.operators import Laplacian
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(Laplacian(C.i))

