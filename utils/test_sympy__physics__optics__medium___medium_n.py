
def test_sympy__physics__optics__medium__MediumN():
    from sympy.physics.optics.medium import Medium
    assert _test_args(Medium('m', n=2))

