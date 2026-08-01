
def test_sympy__physics__optics__gaussopt__BeamParameter():
    from sympy.physics.optics import BeamParameter
    assert _test_args(BeamParameter(530e-9, 1, w=1e-3, n=1))

