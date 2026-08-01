
def test_sympy__physics__units__dimensions__DimensionSystem():
    from sympy.physics.units.dimensions import DimensionSystem
    from sympy.physics.units.definitions.dimension_definitions import length, time, velocity
    assert _test_args(DimensionSystem((length, time), (velocity,)))

