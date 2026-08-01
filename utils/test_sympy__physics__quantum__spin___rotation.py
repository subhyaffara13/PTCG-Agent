
def test_sympy__physics__quantum__spin__Rotation():
    from sympy.physics.quantum.spin import Rotation
    assert _test_args(Rotation(pi, 0, pi/2))

