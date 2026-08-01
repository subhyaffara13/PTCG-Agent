
def test_sympy__vector__orienters__SpaceOrienter():
    from sympy.vector.orienters import SpaceOrienter
    assert _test_args(SpaceOrienter(x, y, z, '123'))

