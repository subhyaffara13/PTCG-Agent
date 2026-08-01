
def test_sympy__vector__orienters__AxisOrienter():
    from sympy.vector.orienters import AxisOrienter
    from sympy.vector.coordsysrect import CoordSys3D
    C = CoordSys3D('C')
    assert _test_args(AxisOrienter(x, C.i))

