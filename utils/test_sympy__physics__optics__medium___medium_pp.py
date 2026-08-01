
def test_sympy__physics__optics__medium__MediumPP():
    from sympy.physics.optics.medium import Medium
    assert _test_args(Medium('m', permittivity=2, permeability=2))

