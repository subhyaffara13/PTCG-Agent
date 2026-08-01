
def test_sympy__vector__orienters__BodyOrienter():
    from sympy.vector.orienters import BodyOrienter
    assert _test_args(BodyOrienter(x, y, z, '123'))

