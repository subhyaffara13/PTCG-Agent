
def test_sympy__physics__units__quantities__PhysicalConstant():
    from sympy.physics.units.quantities import PhysicalConstant
    assert _test_args(PhysicalConstant("foo"))

